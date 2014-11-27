'''
Created on Nov 27, 2014

@author: ivan
'''

# AUTH_PWD_FORM="PWD_FORM"
# AUTH_SAML="SAML"
AUTHENTICATION_TYPE="SAML"

#SAML attribute to use as user ID
SAML_UID_ATTRIBUTE = "uid"


# meta for this SP, can use {} to replace base URL
SAML_META_SP = {
        "entityId": "http://localhost:5000/access/saml/metadata/",
        "assertionConsumerService": {
            "url": "http://localhost:5000/access/saml/sso/acs",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        },
        "singleLogoutService": {
            "url": "http://localhost:5000/access/saml/sso/sls",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "NameIDFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
        "x509cert": "",
        "privateKey": ""
    }

#meta for IDP
SAML_META_IDP = {
        "entityId": "https://localhost:8080/simplesaml/saml2/idp/metadata.php",
        "singleSignOnService": {
            "url": "https://localhost:8080/simplesaml/saml2/idp/SSOService.php",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "singleLogoutService": {
            "url": "https://localhost:8080/simplesaml/saml2/idp/SingleLogoutService.php",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509cert": "MIIDczCCAlugAwIBAgIJAM8CW/7+GjOSMA0GCSqGSIb3DQEBCwUAMFAxCzAJBgNVBAYTAkNaMQ4wDAYDVQQIDAVQcmFoYTEOMAwGA1UEBwwFUHJhaGExDTALBgNVBAoMBFRlc3QxEjAQBgNVBAMMCWxvY2FsaG9zdDAeFw0xNDExMjIxODIyMjNaFw0yNDExMjExODIyMjNaMFAxCzAJBgNVBAYTAkNaMQ4wDAYDVQQIDAVQcmFoYTEOMAwGA1UEBwwFUHJhaGExDTALBgNVBAoMBFRlc3QxEjAQBgNVBAMMCWxvY2FsaG9zdDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALCsxnlh5N5QDeJwIxkXATdyXmanTY6lqd+56hJ3RTwMnv2dD5IrqHxvSNQzZIHPAJLuw7t3DjxVc++Yc8yv9BY5x60XertNbeKmFDoc9Lpc7CTHv70tEz81VjHDxGYfpBe4Z2o/Zjkwb+i1OIp0XHMv30iULF8VbnQdu/f/GCNb/HMQI0fTc2nAJLy35FFLAvwD8ypXIKuKIXLlkvtR4VGGp2CBGjecFrVObAD2Okt/xOz39sYsI5RHVHsb39lh8qIfmb0wSkGXJXaJLfCb0yewOYsUEmf31qidfN9goUoIHvgQ7ugwp8KF6jvgXFOwZ6p4QbbxzoUXbldUPYbLwYUCAwEAAaNQME4wHQYDVR0OBBYEFPRonXoC/zXSecBpN7huzmgY+0NhMB8GA1UdIwQYMBaAFPRonXoC/zXSecBpN7huzmgY+0NhMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAA8REtyOzvaZssyMTeMJR1yp2GQPqeSFuQWt6uRmFf46n4xwi6gwLc6iDm1t0AMSvN9oZQ1DijYmP3Nud7pHPTmX1egkehRd1nndf2tTSds1lvNtEc9SnKp8Poh9F6pQj5ZgBC6QOJRE78df9jZX4/nywT+KVlUrlEUaLBiSrNShYxSZpPJe6Z8kbkyTsTDfwecVwpgCujoroJTUHR51pV7mqi9kqtyyPp5QjH3Lybyj4JL10/iwUWQRYu9bhwRxfGFOMv08cyYkVoMenKyEZFSgVpRTatxS1JFEsxr0RObXvyN0INCXXCXe4xWeEyYucUqW81LYejOfYKopELuqIRU="
    }

#advanced SAML configuration - see python-saml documentation for details
SAML_ADVANCED_CONFIG = {
    "strict": True,
    "debug": True,
    "security": {
        "nameIdEncrypted": False,
        "authnRequestsSigned": False,
        "logoutRequestSigned": False,
        "logoutResponseSigned": False,
        "signMetadata": False,
        "wantMessagesSigned": False,
        "wantAssertionsSigned": False,
        "wantNameIdEncrypted": False
    },
    "contactPerson": {
        "technical": {
            "givenName": "admin",
            "emailAddress": "admin@example.com"
        },
        "support": {
            "givenName": "support",
            "emailAddress": "support@example.com"
        }
    },
    "organization": {
        "en-US": {
            "name": "TEST",
            "displayname": "TEST",
            "url": "http://example.com"
        }
    }
}






