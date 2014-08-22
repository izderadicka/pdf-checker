
$(function() {
    //PDFJS.disableWorker = true;

    var pdfDoc = null,
        pageNum = 1,
        pageRendering = false,
        pageNumPending = null,
        scale = 1.2,
        canvas = document.getElementById('the-canvas'),
        ctx = canvas.getContext('2d');

    /**
     * Get page info from document, resize canvas accordingly, and render page.
     * @param num Page number.
     */
    function renderPage(num) {
      pageRendering = true;
      // Using promise to fetch the page
      pdfDoc.getPage(num).then(function(page) {
        var viewport = page.getViewport(scale);
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // Render PDF page into canvas context
        var renderContext = {
          canvasContext: ctx,
          viewport: viewport
        };
        var renderTask = page.render(renderContext);
        
        // Wait for rendering to finish
        renderTask.promise.then(function () {
          highlightError(viewport.width, viewport.height, scale);
          pageRendering = false;
          if (pageNumPending !== null) {
            // New page rendering is pending
            renderPage(pageNumPending);
            pageNumPending = null;
          }
        });
      });

      // Update page counters
      document.getElementById('page_num').textContent = pageNum;
    }
    
    /**
     * If another page rendering in progress, waits until the rendering is
     * finished. Otherwise, executes rendering immediately.
     */
    function queueRenderPage(num) {
      if (pageRendering) {
        pageNumPending = num;
      } else {
        renderPage(num);
      }
    }

    /**
     * Displays previous page.
     */
    function onPrevPage() {
      if (pageNum <= 1) {
        return;
      }
      pageNum--;
      queueRenderPage(pageNum);
    }

    /**
     * Displays next page.
     */
    function onNextPage() {
      if (pageNum >= pdfDoc.numPages) {
        return;
      }
      pageNum++;
      queueRenderPage(pageNum);
    }
    
    //Diplaying checks
    function displayChecks() {
    	
    	for (var i=0;i<checkResult.length;i++) {
    		var check=checkResult[i],
    		item= '<li data-check="'+i+'">'+check.check_name;
    		if (check.problems.length>0) {
    			item += '<span class="check-result failed">FAILED ('+check.problems.length+')</span>'
    		} else {
    			item+= '<span class="check-result ok">OK</span>'
    		}
    		item+='</li>';
    		
    		$('#checks-list').append($(item))
    	}
    };
    
    function selectCheck(box) {
    	var problems=[],
    	box=$(box),
    	idx=box.attr('data-check') || -1;
    	idx=parseInt(idx);
    	$('#checks-list li').removeClass('selected');
    	$('#all-checks').removeClass('selected');
    	box.addClass('selected');
    			
    	if (idx === -1) {
    		for (var i=0;i<checkResult.length;i++) {
        		var check=checkResult[i];
        		problems=problems.concat(check.problems)
    		}
    	} else {
    		problems=checkResult[idx].problems;
    	}
    	problems.sort(function(a,b) {
    		if (a.page<b.page) {
    			return -1;
    		} else if (a.page>b.page) {
    			return 1
    		} else if (a.top<b.top) {
    			return -1
    		} else if (a.top > b.top) {
    			return 1
    		} else {
    			return 0
    		}
    	});
    	$('#errors-list').empty()
    	for (var j=0; j< problems.length; j++) {
    		var p= problems[j],
    		item='<li>'+'<span class="pos"><span class="page">'+p.page+'</span><span class="top">'+Math.round(p.top)+
    			'</span></span>'+p.text+'</li>',
    		$item=$(item);
    		$item.data('problem', p);
    		$('#errors-list').append($item);
    	};
    	var firstError=$('#errors-list li:first');
    	if (pdfDoc) selectError(firstError);
    	
    };
    
    function selectError(box) {
    	var box=$(box),
    	problem=box.data('problem');
    	$('#errors-list li').removeClass('selected');
    	box.addClass('selected');
    	if (problem) {
    	pageNum=problem.page;
    	errorHighlight={page:problem.page, bbox:problem.bbox, top:problem.top};
    	queueRenderPage(problem.page);
    	
    	} else {
    		pageNum=1;
    		errorHighlight=null;
    		queueRenderPage(pageNum);
    		
    	}
    	
    };
    
    var errorHighlight=null;
    
    function highlightError(width, height, scale) {
    	var e=errorHighlight
    	if ( e && e.page == pageNum) {
    		var ctx=$('#the-canvas').get(0).getContext('2d');
    		ctx.strokeStyle="#FF0000";
    		var x=e.bbox[0]* scale,
    		y = height-e.bbox[1] * scale,
    		w = (e.bbox[2] - e.bbox[0]) * scale,
    		h = (e.bbox[1]-e.bbox[3]) * scale;
    		ctx.strokeRect(x,y, w, h);
    		
    		var scrollTo = height * e.top / 100.0 - 30;
    		$('#page-area').scrollTop(scrollTo);
    		
    	}
    }
    
    //Init code
    
    displayChecks();
    selectCheck($('#all-checks'));
    $('#checks-list').on('click', 'li', function(evt) {
    	selectCheck(this)
    });
    $('#all-checks').on('click', function(evt) {
    	selectCheck(this);
    });
    
    $('#errors-list').on('click', 'li', function(evt) {
    	selectError(this);
    });
    
    //PDF rendering
    $('#prev').on('click', onPrevPage);
    $('#next').on('click', onNextPage);
    /**
     * Asynchronously downloads PDF.
     */
    PDFJS.getDocument(pdfUrl).then(function (pdfDoc_) {
      pdfDoc = pdfDoc_;
      document.getElementById('page_count').textContent = pdfDoc.numPages;
      // Initial/first page rendering
      var firstError=$('#errors-list li:first');
      selectError(firstError);
    		
    });
    
    
})