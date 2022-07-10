from django.core.exceptions import ObjectDoesNotExist


def core(request) :
    prepend = "https://" if request.is_secure() else "http://"
    host = request.get_host()
    #reg_link  = prepend + host + request.user.user_admin.reg_link
    ctx = {}

    ctx['liquidity'] = 53199180
    ctx['site_name_verbose'] = "GTG Cargoose"
    ctx['site_name'] = "GTG Cargoose"
    ctx['site_name_full'] = "GTG Cargoose"
    ctx['support_email'] = "support@gtgcargoose.com"
    ctx['site_email'] = "support@gtgcargoose.com"
    ctx['site_phone'] = "+3594858"
    ctx['site_whatsapp_no'] = "+66658656fg6"
    ctx['site_address'] = "No 23 winston road new york"

    
    return ctx  


    
        