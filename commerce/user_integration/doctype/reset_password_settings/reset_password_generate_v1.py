import frappe
from frappe import _


# VERSION 1 Load html dan load notification
def load_notification(self, version = 1):
    if not self.reset_password_url:
        frappe.throw(_("Please insert reset password url first."))

    social_media_notifications_desktop = ""
    social_media_notifications_mobile = ""
    
    media_social_doc = frappe.get_single("Media Social")
    if media_social_doc:
        if media_social_doc.facebook_url:
            social_media_notifications_desktop += """ <a href="{media_social_url}" target="_blank">
            <img src="{media_social_image}" style="align-items: left; height: 30px;"></a> 
            """.format(media_social_url = media_social_doc.facebook_url, media_social_image = media_social_doc.facebook_logo)
            social_media_notifications_mobile += """ <a href="{media_social_url}" target="_blank"><img src="{media_social_image}" style="height: 30px;"></a>
            """.format(media_social_url = media_social_doc.facebook_url, media_social_image = media_social_doc.facebook_logo)
        if media_social_doc.twitter_url:
            social_media_notifications_desktop += """ <a href="{media_social_url}" target="_blank">
            <img src="{media_social_image}" style="align-items: left; height: 30px;"></a> """.format(media_social_url = media_social_doc.twitter_url, media_social_image = media_social_doc.twitter_logo)
            social_media_notifications_mobile += """ <a href="{media_social_url}" target="_blank"><img src="{media_social_image}" style="height: 30px;"></a>
            """.format(media_social_url = media_social_doc.twitter_url, media_social_image = media_social_doc.twitter_logo)
        if media_social_doc.instagram_url:
            social_media_notifications_desktop += """ <a href="{media_social_url}" target="_blank">
            <img src="{media_social_image}" style="align-items: left; height: 30px;"></a> """.format(media_social_url = media_social_doc.instagram_url, media_social_image = media_social_doc.instagram_logo)
            social_media_notifications_mobile += """ <a href="{media_social_url}" target="_blank"><img src="{media_social_image}" style="height: 30px;"></a>
            """.format(media_social_url = media_social_doc.instagram_url, media_social_image = media_social_doc.instagram_logo)
        if media_social_doc.youtube_url:
            social_media_notifications_desktop += """ <a href="{media_social_url}" target="_blank">
            <img src="{media_social_image}" style="align-items: left; height: 30px;"></a> """.format(media_social_url = media_social_doc.youtube_url, media_social_image = media_social_doc.youtube_logo)
            social_media_notifications_mobile += """ <a href="{media_social_url}" target="_blank"><img src="{media_social_image}" style="height: 30px;"></a>
            """.format(media_social_url = media_social_doc.youtube_url, media_social_image = media_social_doc.youtube_logo)

    app_version_doc = frappe.get_single("App Version")
    download_application = ""
    if app_version_doc:
        if app_version_doc.get("android_play_store_link") and app_version_doc.get("android_play_store_logo") :
            download_application += """ <a href = '{href}' > <img src="{imgSrc}" style="align-items: left; height: 30px;"> </a> """.format(
                 href = app_version_doc.get("android_play_store_link"),
                imgSrc= app_version_doc.get("android_play_store_logo")
            )
        if app_version_doc.get("ios_app_store_link") and app_version_doc.get("ios_app_store_logo"):
            download_application += """ <a href = '{href}' > <img src="{imgSrc}" style="align-items: left; height: 30px;"> </a>""".format(
                href = app_version_doc.get("ios_app_store_link"),
                imgSrc= app_version_doc.get("ios_app_store_logo")
            )

            


        

    
    message = """
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style type="text/css">
        .desktop {
            display: block;
        }
        .hp {
            display: none;
        }

        @media only screen and (max-width: 600px) {
            .desktop {
                display: none;
            }
            .hp {
                display: block;
            }
        }
    </style>
    {% set doc_application_info = frappe.get_doc("Application Info","Application Info") %}
    {% set doc_reset_password_settings = frappe.get_doc("Reset Password Settings","Reset Password Settings") %}
    <center>
        <table style="max-width: 500px;">
            <tr style="background-color: {{doc_application_info.color_primary}}">
                <td style="padding: 10px; padding-left: 20px;text-align:center;">
                    <img src="{{doc_application_info.banner_image}}" style="align-items: center; width: 200px;">
                </td>
            </tr>
            <tr style="background-color: white;">
                <td style="padding: 0px 30px 15px 30px;">
                    <p style="font-size: 24px; font-weight: bold; text-align: left; margin-top: 15px;">
                        Hi, {{ doc.customer_name }}
                    </p>
                    <p style="font-size: 16px; color: {{doc_application_info.font_color_default}}; text-align: left; font-weight: bold;">
                        We received a request to reset your password
                    </p>
                    <p style="font-size: 14px; color: {{doc_application_info.font_color_default}}; text-align: left;">
                        Click the button below to reset your password:
                    </p>

                    <table style="width: 100%; font-size: 13px; border-spacing: 0px 1px; padding: 0px 10px 0px 7px;">
                        <tr style="background-color: {{doc_application_info.color_primary}}">
                            <td rowspan="2" style="width: 2px; background-color:{{doc_application_info.color_primary}};">

                            </td>
                            <td rowspan="2" style="width: 2px; background-color: white">

                            </td>
                            <td style="padding: 10px; font-weight: bold; border-radius: 5px;">
                                <center>
                                    <a style="text-decoration: none; color: white;" href='{{doc_reset_password_settings.reset_password_url}}?key={{doc.key_request}}' target="_blank">
                                        <div class="button-main" link="#ffffff" vlink="#ffffff" alink="#ffffff">
                                            Reset Password
                                        </div>
                                    </a>
                                </center>
                            </td>
                        </tr>
                    </table>

                    <div style="background-color: {{doc_application_info.color_secondary}}; margin-top: 10px; padding: 1px 10px 1px 10px; border-radius: 5px; border: 1px solid; border-color: #DCF2FD;">
                        <p style="font-style: italic; font-size: 12px; color: black;">
                            You're getting this email to make sure it was you. If this is not you, please contact us!
                        </p>
                    </div>
                </td>
            </tr>
            {% set year = frappe.utils.now_datetime().strftime("%Y") %}
            <tr style="background-color: #EEEEEE;">
                <!-- hp -->
                <td  class="hp" style="padding: 15px; text-align: center;">
                    <div style="justify-content: center; margin: 0px;">
                        """ + download_application + """
                    </div>
                    <div style="justify-content: center; margin: 0px;">
                        """ + social_media_notifications_mobile + """
                    </div>
                    <p style="font-size: 12px; color: grey;">
                        Copyright © {{year}} - {{doc_application_info.app_name}}
                    </p>
                </td>

                <!-- desktop -->
                <td class="desktop" style="padding: 15px; text-align: center;">
                    <table style="width: 100%; justify-content: center;">
                        <tr>
                            <td style="text-align: left;">
                                """ + download_application + """
                            </td>
                            <td style="text-align: center;">

                            </td>
                            <td style="text-align: right;">
                                """ + social_media_notifications_desktop + """
                            </td>
                        </tr>
                    </table>
                    <p style="font-size: 12px; color: grey;">
                        Copyright © {{year}} - {{doc_application_info.app_name}}
                    </p>
                </td>
            </tr>
        </table>
    </center>
    """
    return message


def load_html(self,version=1):
    if version == 1:
        if not self.module_name:
            frappe.throw(_("Please insert module_name first."))
        reset_password_settings = frappe.get_single("Reset Password Settings")
        if not reset_password_settings.url_frappe:
            frappe.throw(_("Please set up url frappe"))
        if not reset_password_settings.module_name:
            frappe.throw(_("Please set up module name"))
        if not reset_password_settings.login_site:
            frappe.throw(_("Please set up login_site"))
        reset_password_html = """ <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width,initial-scale=1.0">
            <title>Reset Password</title>
            <link rel="shortcut icon" href="/files/logo.png" type="image/x-icon">


            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
            <style type="text/css">
                :root {
                    --blue: #007bff;
                    --indigo: #6610f2;
                    --purple: #6f42c1;
                    --pink: #e83e8c;
                    --red: #dc3545;
                    --orange: #fd7e14;
                    --yellow: #ffc107;
                    --green: #28a745;
                    --teal: #20c997;
                    --cyan: #17a2b8;
                    --white: #fff;
                    --gray: #6c757d;
                    --gray-dark: #343a40;
                    --primary: #007bff;
                    --secondary: #6c757d;
                    --success: #28a745;
                    --info: #17a2b8;
                    --warning: #ffc107;
                    --danger: #dc3545;
                    --light: #f8f9fa;
                    --dark: #343a40;
                    --breakpoint-xs: 0;
                    --breakpoint-sm: 576px;
                    --breakpoint-md: 768px;
                    --breakpoint-lg: 992px;
                    --breakpoint-xl: 1200px;
                    --font-family-sans-serif: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
                    --font-family-monospace: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace
                }

                *,
                ::after,
                ::before {
                    -webkit-box-sizing: border-box;
                    box-sizing: border-box
                }

                html {
                    font-family: sans-serif;
                    line-height: 1.15;
                    -webkit-text-size-adjust: 100%;
                    -webkit-tap-highlight-color: transparent
                }

                footer {
                    display: block
                }



                [tabindex="-1"]:focus:not(:focus-visible) {
                    outline: 0 !important
                }

                h1,
                h2,
                h3,
                h4,
                h5,
                h6 {
                    margin-top: 0;
                    margin-bottom: .5rem
                }

                p {
                    margin-top: 0;
                    margin-bottom: 1rem
                }

                strong {
                    font-weight: bolder
                }

                a {
                    color: #007bff;
                    text-decoration: none;
                    background-color: transparent
                }

                a:hover {
                    color: #0056b3;
                    text-decoration: underline
                }

                a:not([href]) {
                    color: inherit;
                    text-decoration: none
                }

                a:not([href]):hover {
                    color: inherit;
                    text-decoration: none
                }

                img {
                    vertical-align: middle;
                    border-style: none
                }

                label {
                    display: inline-block;
                    margin-bottom: .5rem
                }

                button {
                    border-radius: 0
                }

                button:focus {
                    outline: 1px dotted;
                    outline: 5px auto -webkit-focus-ring-color
                }

                button,
                input {
                    margin: 0;
                    font-family: inherit;
                    font-size: inherit;
                    line-height: inherit
                }

                button,
                input {
                    overflow: visible
                }

                button {
                    text-transform: none
                }

                [type=button],
                [type=reset],
                [type=submit],
                button {
                    -webkit-appearance: button
                }

                [type=button]:not(:disabled),
                [type=reset]:not(:disabled),
                [type=submit]:not(:disabled),
                button:not(:disabled) {
                    cursor: pointer
                }

                [type=button]::-moz-focus-inner,
                [type=reset]::-moz-focus-inner,
                [type=submit]::-moz-focus-inner,
                button::-moz-focus-inner {
                    padding: 0;
                    border-style: none
                }

                input[type=checkbox],
                input[type=radio] {
                    -webkit-box-sizing: border-box;
                    box-sizing: border-box;
                    padding: 0
                }

                input[type=date],
                input[type=datetime-local],
                input[type=month],
                input[type=time] {
                    -webkit-appearance: listbox
                }

                [type=number]::-webkit-inner-spin-button,
                [type=number]::-webkit-outer-spin-button {
                    height: auto
                }

                [type=search] {
                    outline-offset: -2px;
                    -webkit-appearance: none
                }

                [type=search]::-webkit-search-decoration {
                    -webkit-appearance: none
                }

                ::-webkit-file-upload-button {
                    font: inherit;
                    -webkit-appearance: button
                }

                [hidden] {
                    display: none !important
                }

                .h1,
                .h2,
                .h3,
                .h4,
                .h5,
                .h6,
                h1,
                h2,
                h3,
                h4,
                h5,
                h6 {
                    margin-bottom: .5rem;
                    font-weight: 500;
                    line-height: 1.2
                }

                .h1,
                h1 {
                    font-size: 2.5rem
                }

                .h2,
                h2 {
                    font-size: 2rem
                }

                .h3,
                h3 {
                    font-size: 1.75rem
                }

                .h4,
                h4 {
                    font-size: 1.5rem
                }

                .h5,
                h5 {
                    font-size: 1.25rem
                }

                .h6,
                h6 {
                    font-size: 1rem
                }

                .display-1 {
                    font-size: 6rem;
                    font-weight: 300;
                    line-height: 1.2
                }

                .display-2 {
                    font-size: 5.5rem;
                    font-weight: 300;
                    line-height: 1.2
                }

                .display-3 {
                    font-size: 4.5rem;
                    font-weight: 300;
                    line-height: 1.2
                }

                .display-4 {
                    font-size: 3.5rem;
                    font-weight: 300;
                    line-height: 1.2
                }

                .container {
                    width: 100%;
                    padding-right: 15px;
                    padding-left: 15px;
                    margin-right: auto;
                    margin-left: auto
                }

                @media (min-width:576px) {
                    .container {
                        max-width: 540px
                    }
                }

                @media (min-width:768px) {
                    .container {
                        max-width: 720px
                    }
                }

                @media (min-width:992px) {
                    .container {
                        max-width: 960px
                    }
                }

                @media (min-width:1200px) {
                    .container {
                        max-width: 1140px
                    }
                }

                .container-lg,
                .container-md,
                .container-sm {
                    width: 100%;
                    padding-right: 15px;
                    padding-left: 15px;
                    margin-right: auto;
                    margin-left: auto
                }

                @media (min-width:576px) {

                    .container,
                    .container-sm {
                        max-width: 540px
                    }
                }

                @media (min-width:768px) {

                    .container,
                    .container-md,
                    .container-sm {
                        max-width: 720px
                    }
                }

                @media (min-width:992px) {

                    .container,
                    .container-lg,
                    .container-md,
                    .container-sm {
                        max-width: 960px
                    }
                }

                @media (min-width:1200px) {

                    .container,
                    .container-lg,
                    .container-md,
                    .container-sm {
                        max-width: 1140px
                    }
                }

                .row {
                    display: -ms-flexbox;
                    display: -webkit-box;
                    display: flex;
                    -ms-flex-wrap: wrap;
                    flex-wrap: wrap;
                    margin-right: -15px;
                    margin-left: -15px
                }

                .col,
                .col-1,
                .col-10,
                .col-11,
                .col-12,
                .col-2,
                .col-3,
                .col-4,
                .col-5,
                .col-6,
                .col-7,
                .col-8,
                .col-9,
                .col-lg,
                .col-lg-1,
                .col-lg-10,
                .col-lg-11,
                .col-lg-12,
                .col-lg-2,
                .col-lg-3,
                .col-lg-4,
                .col-lg-5,
                .col-lg-6,
                .col-lg-7,
                .col-lg-8,
                .col-lg-9,
                .col-md,
                .col-md-1,
                .col-md-10,
                .col-md-11,
                .col-md-12,
                .col-md-2,
                .col-md-3,
                .col-md-4,
                .col-md-5,
                .col-md-6,
                .col-md-7,
                .col-md-8,
                .col-md-9,
                .col-sm,
                .col-sm-1,
                .col-sm-10,
                .col-sm-11,
                .col-sm-12,
                .col-sm-2,
                .col-sm-3,
                .col-sm-4,
                .col-sm-5,
                .col-sm-6,
                .col-sm-7,
                .col-sm-8,
                .col-sm-9 {
                    position: relative;
                    width: 100%;
                    padding-right: 15px;
                    padding-left: 15px
                }

                .col {
                    -ms-flex-preferred-size: 0;
                    flex-basis: 0;
                    -ms-flex-positive: 1;
                    -webkit-box-flex: 1;
                    flex-grow: 1;
                    max-width: 100%
                }

                .col-1 {
                    -ms-flex: 0 0 8.333333%;
                    -webkit-box-flex: 0;
                    flex: 0 0 8.333333%;
                    max-width: 8.333333%
                }

                .col-2 {
                    -ms-flex: 0 0 16.666667%;
                    -webkit-box-flex: 0;
                    flex: 0 0 16.666667%;
                    max-width: 16.666667%
                }

                .col-3 {
                    -ms-flex: 0 0 25%;
                    -webkit-box-flex: 0;
                    flex: 0 0 25%;
                    max-width: 25%
                }

                .col-4 {
                    -ms-flex: 0 0 33.333333%;
                    -webkit-box-flex: 0;
                    flex: 0 0 33.333333%;
                    max-width: 33.333333%
                }

                .col-5 {
                    -ms-flex: 0 0 41.666667%;
                    -webkit-box-flex: 0;
                    flex: 0 0 41.666667%;
                    max-width: 41.666667%
                }

                .col-6 {
                    -ms-flex: 0 0 50%;
                    -webkit-box-flex: 0;
                    flex: 0 0 50%;
                    max-width: 50%
                }

                .col-7 {
                    -ms-flex: 0 0 58.333333%;
                    -webkit-box-flex: 0;
                    flex: 0 0 58.333333%;
                    max-width: 58.333333%
                }

                .col-8 {
                    -ms-flex: 0 0 66.666667%;
                    -webkit-box-flex: 0;
                    flex: 0 0 66.666667%;
                    max-width: 66.666667%
                }

                .col-9 {
                    -ms-flex: 0 0 75%;
                    -webkit-box-flex: 0;
                    flex: 0 0 75%;
                    max-width: 75%
                }

                .col-10 {
                    -ms-flex: 0 0 83.333333%;
                    -webkit-box-flex: 0;
                    flex: 0 0 83.333333%;
                    max-width: 83.333333%
                }

                .col-11 {
                    -ms-flex: 0 0 91.666667%;
                    -webkit-box-flex: 0;
                    flex: 0 0 91.666667%;
                    max-width: 91.666667%
                }

                .col-12 {
                    -ms-flex: 0 0 100%;
                    -webkit-box-flex: 0;
                    flex: 0 0 100%;
                    max-width: 100%
                }

                @media (min-width:576px) {
                    .col-sm {
                        -ms-flex-preferred-size: 0;
                        flex-basis: 0;
                        -ms-flex-positive: 1;
                        -webkit-box-flex: 1;
                        flex-grow: 1;
                        max-width: 100%
                    }

                    .col-sm-1 {
                        -ms-flex: 0 0 8.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 8.333333%;
                        max-width: 8.333333%
                    }

                    .col-sm-2 {
                        -ms-flex: 0 0 16.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 16.666667%;
                        max-width: 16.666667%
                    }

                    .col-sm-3 {
                        -ms-flex: 0 0 25%;
                        -webkit-box-flex: 0;
                        flex: 0 0 25%;
                        max-width: 25%
                    }

                    .col-sm-4 {
                        -ms-flex: 0 0 33.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 33.333333%;
                        max-width: 33.333333%
                    }

                    .col-sm-5 {
                        -ms-flex: 0 0 41.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 41.666667%;
                        max-width: 41.666667%
                    }

                    .col-sm-6 {
                        -ms-flex: 0 0 50%;
                        -webkit-box-flex: 0;
                        flex: 0 0 50%;
                        max-width: 50%
                    }

                    .col-sm-7 {
                        -ms-flex: 0 0 58.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 58.333333%;
                        max-width: 58.333333%
                    }

                    .col-sm-8 {
                        -ms-flex: 0 0 66.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 66.666667%;
                        max-width: 66.666667%
                    }

                    .col-sm-9 {
                        -ms-flex: 0 0 75%;
                        -webkit-box-flex: 0;
                        flex: 0 0 75%;
                        max-width: 75%
                    }

                    .col-sm-10 {
                        -ms-flex: 0 0 83.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 83.333333%;
                        max-width: 83.333333%
                    }

                    .col-sm-11 {
                        -ms-flex: 0 0 91.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 91.666667%;
                        max-width: 91.666667%
                    }

                    .col-sm-12 {
                        -ms-flex: 0 0 100%;
                        -webkit-box-flex: 0;
                        flex: 0 0 100%;
                        max-width: 100%
                    }
                }

                @media (min-width:768px) {
                    .col-md {
                        -ms-flex-preferred-size: 0;
                        flex-basis: 0;
                        -ms-flex-positive: 1;
                        -webkit-box-flex: 1;
                        flex-grow: 1;
                        max-width: 100%
                    }

                    .col-md-1 {
                        -ms-flex: 0 0 8.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 8.333333%;
                        max-width: 8.333333%
                    }

                    .col-md-2 {
                        -ms-flex: 0 0 16.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 16.666667%;
                        max-width: 16.666667%
                    }

                    .col-md-3 {
                        -ms-flex: 0 0 25%;
                        -webkit-box-flex: 0;
                        flex: 0 0 25%;
                        max-width: 25%
                    }

                    .col-md-4 {
                        -ms-flex: 0 0 33.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 33.333333%;
                        max-width: 33.333333%
                    }

                    .col-md-5 {
                        -ms-flex: 0 0 41.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 41.666667%;
                        max-width: 41.666667%
                    }

                    .col-md-6 {
                        -ms-flex: 0 0 50%;
                        -webkit-box-flex: 0;
                        flex: 0 0 50%;
                        max-width: 50%
                    }

                    .col-md-7 {
                        -ms-flex: 0 0 58.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 58.333333%;
                        max-width: 58.333333%
                    }

                    .col-md-8 {
                        -ms-flex: 0 0 66.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 66.666667%;
                        max-width: 66.666667%
                    }

                    .col-md-9 {
                        -ms-flex: 0 0 75%;
                        -webkit-box-flex: 0;
                        flex: 0 0 75%;
                        max-width: 75%
                    }

                    .col-md-10 {
                        -ms-flex: 0 0 83.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 83.333333%;
                        max-width: 83.333333%
                    }

                    .col-md-11 {
                        -ms-flex: 0 0 91.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 91.666667%;
                        max-width: 91.666667%
                    }

                    .col-md-12 {
                        -ms-flex: 0 0 100%;
                        -webkit-box-flex: 0;
                        flex: 0 0 100%;
                        max-width: 100%
                    }
                }

                @media (min-width:992px) {
                    .col-lg {
                        -ms-flex-preferred-size: 0;
                        flex-basis: 0;
                        -ms-flex-positive: 1;
                        -webkit-box-flex: 1;
                        flex-grow: 1;
                        max-width: 100%
                    }

                    .col-lg-1 {
                        -ms-flex: 0 0 8.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 8.333333%;
                        max-width: 8.333333%
                    }

                    .col-lg-2 {
                        -ms-flex: 0 0 16.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 16.666667%;
                        max-width: 16.666667%
                    }

                    .col-lg-3 {
                        -ms-flex: 0 0 25%;
                        -webkit-box-flex: 0;
                        flex: 0 0 25%;
                        max-width: 25%
                    }

                    .col-lg-4 {
                        -ms-flex: 0 0 33.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 33.333333%;
                        max-width: 33.333333%
                    }

                    .col-lg-5 {
                        -ms-flex: 0 0 41.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 41.666667%;
                        max-width: 41.666667%
                    }

                    .col-lg-6 {
                        -ms-flex: 0 0 50%;
                        -webkit-box-flex: 0;
                        flex: 0 0 50%;
                        max-width: 50%
                    }

                    .col-lg-7 {
                        -ms-flex: 0 0 58.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 58.333333%;
                        max-width: 58.333333%
                    }

                    .col-lg-8 {
                        -ms-flex: 0 0 66.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 66.666667%;
                        max-width: 66.666667%
                    }

                    .col-lg-9 {
                        -ms-flex: 0 0 75%;
                        -webkit-box-flex: 0;
                        flex: 0 0 75%;
                        max-width: 75%
                    }

                    .col-lg-10 {
                        -ms-flex: 0 0 83.333333%;
                        -webkit-box-flex: 0;
                        flex: 0 0 83.333333%;
                        max-width: 83.333333%
                    }

                    .col-lg-11 {
                        -ms-flex: 0 0 91.666667%;
                        -webkit-box-flex: 0;
                        flex: 0 0 91.666667%;
                        max-width: 91.666667%
                    }

                    .col-lg-12 {
                        -ms-flex: 0 0 100%;
                        -webkit-box-flex: 0;
                        flex: 0 0 100%;
                        max-width: 100%
                    }
                }

                .form-control {
                    display: block;
                    width: 100%;
                    height: calc(1.5em + .75rem + 2px);
                    padding: .375rem .75rem;
                    font-size: 1rem;
                    font-weight: 400;
                    line-height: 1.5;
                    color: #495057;
                    background-color: #fff;
                    background-clip: padding-box;
                    border: 1px solid #ced4da;
                    border-radius: .25rem;
                    -webkit-transition: border-color .15s ease-in-out, -webkit-box-shadow .15s ease-in-out;
                    transition: border-color .15s ease-in-out, -webkit-box-shadow .15s ease-in-out;
                    transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
                    transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out, -webkit-box-shadow .15s ease-in-out
                }

                @media (prefers-reduced-motion:reduce) {
                    .form-control {
                        -webkit-transition: none;
                        transition: none
                    }
                }

                .form-control::-ms-expand {
                    background-color: transparent;
                    border: 0
                }

                .form-control:-moz-focusring {
                    color: transparent;
                    text-shadow: 0 0 0 #495057
                }

                .form-control:focus {
                    color: #495057;
                    background-color: #fff;
                    border-color: #80bdff;
                    outline: 0;
                    -webkit-box-shadow: 0 0 0 .2rem rgba(0, 123, 255, .25);
                    box-shadow: 0 0 0 .2rem rgba(0, 123, 255, .25)
                }

                .form-control::-webkit-input-placeholder {
                    color: #6c757d;
                    opacity: 1
                }

                .form-control::-moz-placeholder {
                    color: #6c757d;
                    opacity: 1
                }

                .form-control:-ms-input-placeholder {
                    color: #6c757d;
                    opacity: 1
                }

                .form-control::-ms-input-placeholder {
                    color: #6c757d;
                    opacity: 1
                }

                .form-control::placeholder {
                    color: #6c757d;
                    opacity: 1
                }

                .form-control:disabled,
                .form-control[readonly] {
                    background-color: #e9ecef;
                    opacity: 1
                }

                .col-form-label {
                    padding-top: calc(.375rem + 1px);
                    padding-bottom: calc(.375rem + 1px);
                    margin-bottom: 0;
                    font-size: inherit;
                    line-height: 1.5
                }

                .col-form-label-lg {
                    padding-top: calc(.5rem + 1px);
                    padding-bottom: calc(.5rem + 1px);
                    font-size: 1.25rem;
                    line-height: 1.5
                }

                .col-form-label-sm {
                    padding-top: calc(.25rem + 1px);
                    padding-bottom: calc(.25rem + 1px);
                    font-size: .875rem;
                    line-height: 1.5
                }

                .form-control-sm {
                    height: calc(1.5em + .5rem + 2px);
                    padding: .25rem .5rem;
                    font-size: .875rem;
                    line-height: 1.5;
                    border-radius: .2rem
                }

                .form-control-lg {
                    height: calc(1.5em + 1rem + 2px);
                    padding: .5rem 1rem;
                    font-size: 1.25rem;
                    line-height: 1.5;
                    border-radius: .3rem
                }

                .form-group {
                    margin-bottom: 1rem
                }

                .form-text {
                    display: block;
                    margin-top: .25rem
                }

                .form-row {
                    display: -ms-flexbox;
                    display: -webkit-box;
                    display: flex;
                    -ms-flex-wrap: wrap;
                    flex-wrap: wrap;
                    margin-right: -5px;
                    margin-left: -5px
                }

                .form-row>.col,
                .form-row>[class*=col-] {
                    padding-right: 5px;
                    padding-left: 5px
                }

                .form-inline {
                    display: -ms-flexbox;
                    display: -webkit-box;
                    display: flex;
                    -ms-flex-flow: row wrap;
                    -webkit-box-orient: horizontal;
                    -webkit-box-direction: normal;
                    flex-flow: row wrap;
                    -ms-flex-align: center;
                    -webkit-box-align: center;
                    align-items: center
                }

                @media (min-width:576px) {
                    .form-inline label {
                        display: -ms-flexbox;
                        display: -webkit-box;
                        display: flex;
                        -ms-flex-align: center;
                        -webkit-box-align: center;
                        align-items: center;
                        -ms-flex-pack: center;
                        -webkit-box-pack: center;
                        justify-content: center;
                        margin-bottom: 0
                    }

                    .form-inline .form-group {
                        display: -ms-flexbox;
                        display: -webkit-box;
                        display: flex;
                        -ms-flex: 0 0 auto;
                        -webkit-box-flex: 0;
                        flex: 0 0 auto;
                        -ms-flex-flow: row wrap;
                        -webkit-box-orient: horizontal;
                        -webkit-box-direction: normal;
                        flex-flow: row wrap;
                        -ms-flex-align: center;
                        -webkit-box-align: center;
                        align-items: center;
                        margin-bottom: 0
                    }

                    .form-inline .form-control {
                        display: inline-block;
                        width: auto;
                        vertical-align: middle
                    }

                    .form-inline .input-group {
                        width: auto
                    }
                }

                .btn {
                    display: inline-block;
                    font-weight: 400;
                    color: #212529;
                    text-align: center;
                    vertical-align: middle;
                    cursor: pointer;
                    -webkit-user-select: none;
                    -moz-user-select: none;
                    -ms-user-select: none;
                    user-select: none;
                    background-color: transparent;
                    border: 1px solid transparent;
                    padding: .375rem .75rem;
                    font-size: 1rem;
                    line-height: 1.5;
                    border-radius: .25rem;
                    -webkit-transition: color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, -webkit-box-shadow .15s ease-in-out;
                    transition: color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, -webkit-box-shadow .15s ease-in-out;
                    transition: color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
                    transition: color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out, -webkit-box-shadow .15s ease-in-out
                }

                @media (prefers-reduced-motion:reduce) {
                    .btn {
                        -webkit-transition: none;
                        transition: none
                    }
                }

                .btn:hover {
                    color: #212529;
                    text-decoration: none
                }

                .btn:focus {
                    outline: 0;
                    -webkit-box-shadow: 0 0 0 .2rem rgba(0, 123, 255, .25);
                    box-shadow: 0 0 0 .2rem rgba(0, 123, 255, .25)
                }

                .btn:disabled {
                    opacity: .65
                }

                .btn-danger {
                    color: #fff;
                    background-color: #000000;
                    border-color: #ffffff
                }

                .btn-danger:hover {
                    color: #fff;
                    background-color: #000000;
                    border-color: #ffffff
                }

                .btn-danger:focus {
                    color: #fff;
                    background-color: #000000;
                    border-color: #ffffff;
                    /* -webkit-box-shadow: 0 0 0 .2rem rgba(225, 83, 97, .5); */
                    /* box-shadow: 0 0 0 .2rem rgba(225, 83, 97, .5) */
                }

                .btn-danger:disabled {
                    color: #fff;
                    background-color: #000000;
                    border-color: #ffffff;
                }

                .btn-group-lg>.btn,
                .btn-lg {
                    padding: .5rem 1rem;
                    font-size: 1.25rem;
                    line-height: 1.5;
                    border-radius: .3rem
                }

                .btn-group-sm>.btn,
                .btn-sm {
                    padding: .25rem .5rem;
                    font-size: .875rem;
                    line-height: 1.5;
                    border-radius: .2rem
                }

                .btn-block {
                    display: block;
                    width: 100%
                }

                .btn-block+.btn-block {
                    margin-top: .5rem
                }

                input[type=button].btn-block,
                input[type=reset].btn-block,
                input[type=submit].btn-block {
                    width: 100%
                }

                .btn-group {
                    position: relative;
                    display: -ms-inline-flexbox;
                    display: -webkit-inline-box;
                    display: inline-flex;
                    vertical-align: middle
                }

                .btn-group>.btn {
                    position: relative;
                    -ms-flex: 1 1 auto;
                    -webkit-box-flex: 1;
                    flex: 1 1 auto
                }

                .btn-group>.btn:hover {
                    z-index: 1
                }

                .btn-group>.btn:active,
                .btn-group>.btn:focus {
                    z-index: 1
                }

                .btn-group>.btn-group:not(:first-child),
                .btn-group>.btn:not(:first-child) {
                    margin-left: -1px
                }

                .btn-group>.btn-group:not(:last-child)>.btn {
                    border-top-right-radius: 0;
                    border-bottom-right-radius: 0
                }

                .btn-group>.btn-group:not(:first-child)>.btn,
                .btn-group>.btn:not(:first-child) {
                    border-top-left-radius: 0;
                    border-bottom-left-radius: 0
                }

                .input-group {
                    position: relative;
                    display: -ms-flexbox;
                    display: -webkit-box;
                    display: flex;
                    -ms-flex-wrap: wrap;
                    flex-wrap: wrap;
                    -ms-flex-align: stretch;
                    -webkit-box-align: stretch;
                    align-items: stretch;
                    width: 100%
                }

                .input-group>.form-control {
                    position: relative;
                    -ms-flex: 1 1 0%;
                    -webkit-box-flex: 1;
                    flex: 1 1 0%;
                    min-width: 0;
                    margin-bottom: 0
                }

                .input-group>.form-control+.form-control {
                    margin-left: -1px
                }

                .input-group>.form-control:focus {
                    z-index: 3
                }

                .input-group>.form-control:not(:last-child) {
                    border-top-right-radius: 0;
                    border-bottom-right-radius: 0
                }

                .input-group>.form-control:not(:first-child) {
                    border-top-left-radius: 0;
                    border-bottom-left-radius: 0
                }

                .input-group-text {
                    display: -ms-flexbox;
                    display: -webkit-box;
                    display: flex;
                    -ms-flex-align: center;
                    -webkit-box-align: center;
                    align-items: center;
                    padding: .375rem .75rem;
                    margin-bottom: 0;
                    font-size: 1rem;
                    font-weight: 400;
                    line-height: 1.5;
                    color: #495057;
                    text-align: center;
                    white-space: nowrap;
                    background-color: #e9ecef;
                    border: 1px solid #ced4da;
                    border-radius: .25rem
                }

                .input-group-text input[type=checkbox],
                .input-group-text input[type=radio] {
                    margin-top: 0
                }

                .input-group-lg>.form-control:not(textarea) {
                    height: calc(1.5em + 1rem + 2px)
                }

                .input-group-lg>.form-control {
                    padding: .5rem 1rem;
                    font-size: 1.25rem;
                    line-height: 1.5;
                    border-radius: .3rem
                }

                .input-group-sm>.form-control:not(textarea) {
                    height: calc(1.5em + .5rem + 2px)
                }

                .input-group-sm>.form-control {
                    padding: .25rem .5rem;
                    font-size: .875rem;
                    line-height: 1.5;
                    border-radius: .2rem
                }

                .card {
                    position: relative;
                    display: -ms-flexbox;
                    display: -webkit-box;
                    display: flex;
                    -ms-flex-direction: column;
                    -webkit-box-orient: vertical;
                    -webkit-box-direction: normal;
                    flex-direction: column;
                    min-width: 0;
                    word-wrap: break-word;
                    background-color: #fff;
                    background-clip: border-box;
                    border: 1px solid rgba(0, 0, 0, .125);
                    border-radius: .25rem
                }

                .card-body {
                    -ms-flex: 1 1 auto;
                    -webkit-box-flex: 1;
                    flex: 1 1 auto;
                    min-height: 1px;
                    padding: 1.25rem
                }

                .card-text:last-child {
                    margin-bottom: 0
                }

                .card-footer {
                    padding: .75rem 1.25rem;
                    background-color: rgba(0, 0, 0, .03);
                    border-top: 1px solid rgba(0, 0, 0, .125)
                }

                .card-footer:last-child {
                    border-radius: 0 0 calc(.25rem - 1px) calc(.25rem - 1px)
                }

                .card-img,
                .card-img-bottom,
                .card-img-top {
                    -ms-flex-negative: 0;
                    flex-shrink: 0;
                    width: 100%
                }

                .card-img,
                .card-img-top {
                    border-top-left-radius: calc(.25rem - 1px);
                    border-top-right-radius: calc(.25rem - 1px)
                }

                .card-img,
                .card-img-bottom {
                    border-bottom-right-radius: calc(.25rem - 1px);
                    border-bottom-left-radius: calc(.25rem - 1px)
                }

                .card-group>.card {
                    margin-bottom: 15px
                }

                @media (min-width:576px) {
                    .card-group {
                        display: -ms-flexbox;
                        display: -webkit-box;
                        display: flex;
                        -ms-flex-flow: row wrap;
                        -webkit-box-orient: horizontal;
                        -webkit-box-direction: normal;
                        flex-flow: row wrap
                    }

                    .card-group>.card {
                        -ms-flex: 1 0 0%;
                        -webkit-box-flex: 1;
                        flex: 1 0 0%;
                        margin-bottom: 0
                    }

                    .card-group>.card+.card {
                        margin-left: 0;
                        border-left: 0
                    }

                    .card-group>.card:not(:last-child) {
                        border-top-right-radius: 0;
                        border-bottom-right-radius: 0
                    }

                    .card-group>.card:not(:last-child) .card-img-top {
                        border-top-right-radius: 0
                    }

                    .card-group>.card:not(:last-child) .card-footer,
                    .card-group>.card:not(:last-child) .card-img-bottom {
                        border-bottom-right-radius: 0
                    }

                    .card-group>.card:not(:first-child) {
                        border-top-left-radius: 0;
                        border-bottom-left-radius: 0
                    }

                    .card-group>.card:not(:first-child) .card-img-top {
                        border-top-left-radius: 0
                    }

                    .card-group>.card:not(:first-child) .card-footer,
                    .card-group>.card:not(:first-child) .card-img-bottom {
                        border-bottom-left-radius: 0
                    }
                }

                @-webkit-keyframes progress-bar-stripes {
                    from {
                        background-position: 1rem 0
                    }

                    to {
                        background-position: 0 0
                    }
                }

                @keyframes progress-bar-stripes {
                    from {
                        background-position: 1rem 0
                    }

                    to {
                        background-position: 0 0
                    }
                }

                @-webkit-keyframes spinner-border {
                    to {
                        -webkit-transform: rotate(360deg);
                        transform: rotate(360deg)
                    }
                }

                @keyframes spinner-border {
                    to {
                        -webkit-transform: rotate(360deg);
                        transform: rotate(360deg)
                    }
                }

                @-webkit-keyframes spinner-grow {
                    0% {
                        -webkit-transform: scale(0);
                        transform: scale(0)
                    }

                    50% {
                        opacity: 1
                    }
                }

                @keyframes spinner-grow {
                    0% {
                        -webkit-transform: scale(0);
                        transform: scale(0)
                    }

                    50% {
                        opacity: 1
                    }
                }

                .align-top {
                    vertical-align: top !important
                }

                .align-bottom {
                    vertical-align: bottom !important
                }

                .align-text-bottom {
                    vertical-align: text-bottom !important
                }

                .align-text-top {
                    vertical-align: text-top !important
                }

                .bg-danger {
                    background-color: #ffffff !important
                }

                a.bg-danger:focus,
                a.bg-danger:hover,
                button.bg-danger:focus,
                button.bg-danger:hover {
                    background-color: #ffffff !important
                }

                .bg-white {
                    background-color: #fff !important
                }

                .d-none {
                    display: none !important
                }

                .d-inline {
                    display: inline !important
                }

                .d-inline-block {
                    display: inline-block !important
                }

                .d-block {
                    display: block !important
                }

                .d-flex {
                    display: -ms-flexbox !important;
                    display: -webkit-box !important;
                    display: flex !important
                }

                .d-inline-flex {
                    display: -ms-inline-flexbox !important;
                    display: -webkit-inline-box !important;
                    display: inline-flex !important
                }

                @media (min-width:576px) {
                    .d-sm-none {
                        display: none !important
                    }

                    .d-sm-inline {
                        display: inline !important
                    }

                    .d-sm-inline-block {
                        display: inline-block !important
                    }

                    .d-sm-block {
                        display: block !important
                    }

                    .d-sm-flex {
                        display: -ms-flexbox !important;
                        display: -webkit-box !important;
                        display: flex !important
                    }

                    .d-sm-inline-flex {
                        display: -ms-inline-flexbox !important;
                        display: -webkit-inline-box !important;
                        display: inline-flex !important
                    }
                }

                @media (min-width:768px) {
                    .d-md-none {
                        display: none !important
                    }

                    .d-md-inline {
                        display: inline !important
                    }

                    .d-md-inline-block {
                        display: inline-block !important
                    }

                    .d-md-block {
                        display: block !important
                    }

                    .d-md-flex {
                        display: -ms-flexbox !important;
                        display: -webkit-box !important;
                        display: flex !important
                    }

                    .d-md-inline-flex {
                        display: -ms-inline-flexbox !important;
                        display: -webkit-inline-box !important;
                        display: inline-flex !important
                    }
                }

                @media (min-width:992px) {
                    .d-lg-none {
                        display: none !important
                    }

                    .d-lg-inline {
                        display: inline !important
                    }

                    .d-lg-inline-block {
                        display: inline-block !important
                    }

                    .d-lg-block {
                        display: block !important
                    }

                    .d-lg-flex {
                        display: -ms-flexbox !important;
                        display: -webkit-box !important;
                        display: flex !important
                    }

                    .d-lg-inline-flex {
                        display: -ms-inline-flexbox !important;
                        display: -webkit-inline-box !important;
                        display: inline-flex !important
                    }
                }

                .flex-row {
                    -ms-flex-direction: row !important;
                    -webkit-box-orient: horizontal !important;
                    -webkit-box-direction: normal !important;
                    flex-direction: row !important
                }

                .justify-content-center {
                    -ms-flex-pack: center !important;
                    -webkit-box-pack: center !important;
                    justify-content: center !important
                }

                .align-items-center {
                    -ms-flex-align: center !important;
                    -webkit-box-align: center !important;
                    align-items: center !important
                }

                .align-content-center {
                    -ms-flex-line-pack: center !important;
                    align-content: center !important
                }

                @media (min-width:576px) {
                    .flex-sm-row {
                        -ms-flex-direction: row !important;
                        -webkit-box-orient: horizontal !important;
                        -webkit-box-direction: normal !important;
                        flex-direction: row !important
                    }

                    .justify-content-sm-center {
                        -ms-flex-pack: center !important;
                        -webkit-box-pack: center !important;
                        justify-content: center !important
                    }

                    .align-items-sm-center {
                        -ms-flex-align: center !important;
                        -webkit-box-align: center !important;
                        align-items: center !important
                    }

                    .align-content-sm-center {
                        -ms-flex-line-pack: center !important;
                        align-content: center !important
                    }
                }

                @media (min-width:768px) {
                    .flex-md-row {
                        -ms-flex-direction: row !important;
                        -webkit-box-orient: horizontal !important;
                        -webkit-box-direction: normal !important;
                        flex-direction: row !important
                    }

                    .justify-content-md-center {
                        -ms-flex-pack: center !important;
                        -webkit-box-pack: center !important;
                        justify-content: center !important
                    }

                    .align-items-md-center {
                        -ms-flex-align: center !important;
                        -webkit-box-align: center !important;
                        align-items: center !important
                    }

                    .align-content-md-center {
                        -ms-flex-line-pack: center !important;
                        align-content: center !important
                    }
                }

                @media (min-width:992px) {
                    .flex-lg-row {
                        -ms-flex-direction: row !important;
                        -webkit-box-orient: horizontal !important;
                        -webkit-box-direction: normal !important;
                        flex-direction: row !important
                    }

                    .justify-content-lg-center {
                        -ms-flex-pack: center !important;
                        -webkit-box-pack: center !important;
                        justify-content: center !important
                    }

                    .align-items-lg-center {
                        -ms-flex-align: center !important;
                        -webkit-box-align: center !important;
                        align-items: center !important
                    }

                    .align-content-lg-center {
                        -ms-flex-line-pack: center !important;
                        align-content: center !important
                    }
                }

                .position-relative {
                    position: relative !important
                }

                .position-absolute {
                    position: absolute !important
                }

                .position-fixed {
                    position: fixed !important
                }

                .fixed-top {
                    position: fixed;
                    top: 0;
                    right: 0;
                    left: 0;
                    z-index: 1030
                }

                .fixed-bottom {
                    position: fixed;
                    right: 0;
                    bottom: 0;
                    left: 0;
                    z-index: 1030
                }

                @supports ((position:-webkit-sticky) or (position:sticky)) {
                    .sticky-top {
                        position: -webkit-sticky;
                        position: sticky;
                        top: 0;
                        z-index: 1020
                    }
                }

                .shadow-sm {
                    -webkit-box-shadow: 0 .125rem .25rem rgba(0, 0, 0, .075) !important;
                    box-shadow: 0 .125rem .25rem rgba(0, 0, 0, .075) !important
                }

                .shadow {
                    -webkit-box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .15) !important;
                    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .15) !important
                }

                .shadow-lg {
                    -webkit-box-shadow: 0 1rem 3rem rgba(0, 0, 0, .175) !important;
                    box-shadow: 0 1rem 3rem rgba(0, 0, 0, .175) !important
                }

                .shadow-none {
                    -webkit-box-shadow: none !important;
                    box-shadow: none !important
                }

                .w-25 {
                    width: 25% !important
                }

                .w-50 {
                    width: 50% !important
                }

                .w-75 {
                    width: 75% !important
                }

                .w-100 {
                    width: 100% !important
                }

                .h-25 {
                    height: 25% !important
                }

                .h-50 {
                    height: 50% !important
                }

                .h-75 {
                    height: 75% !important
                }

                .h-100 {
                    height: 100% !important
                }

                .mt-0 {
                    margin-top: 0 !important
                }

                .mb-0 {
                    margin-bottom: 0 !important
                }

                .mt-1 {
                    margin-top: .25rem !important
                }

                .mb-1 {
                    margin-bottom: .25rem !important
                }

                .mt-2 {
                    margin-top: .5rem !important
                }

                .mb-2 {
                    margin-bottom: .5rem !important
                }

                .mt-3 {
                    margin-top: 1rem !important
                }

                .mb-3 {
                    margin-bottom: 1rem !important
                }

                .mt-4 {
                    margin-top: 1.5rem !important
                }

                .mb-4 {
                    margin-bottom: 1.5rem !important
                }

                .mt-5 {
                    margin-top: 3rem !important
                }

                .mb-5 {
                    margin-bottom: 3rem !important
                }

                .p-0 {
                    padding: 0 !important
                }

                .pr-0,
                .px-0 {
                    padding-right: 0 !important
                }

                .pl-0,
                .px-0 {
                    padding-left: 0 !important
                }

                .p-1 {
                    padding: .25rem !important
                }

                .pr-1,
                .px-1 {
                    padding-right: .25rem !important
                }

                .pl-1,
                .px-1 {
                    padding-left: .25rem !important
                }

                .p-2 {
                    padding: .5rem !important
                }

                .pr-2,
                .px-2 {
                    padding-right: .5rem !important
                }

                .pl-2,
                .px-2 {
                    padding-left: .5rem !important
                }

                .p-3 {
                    padding: 1rem !important
                }

                .pr-3,
                .px-3 {
                    padding-right: 1rem !important
                }

                .pl-3,
                .px-3 {
                    padding-left: 1rem !important
                }

                .p-4 {
                    padding: 1.5rem !important
                }

                .pr-4,
                .px-4 {
                    padding-right: 1.5rem !important
                }

                .pl-4,
                .px-4 {
                    padding-left: 1.5rem !important
                }

                .p-5 {
                    padding: 3rem !important
                }

                .pr-5,
                .px-5 {
                    padding-right: 3rem !important
                }

                .pl-5,
                .px-5 {
                    padding-left: 3rem !important
                }

                @media (min-width:576px) {
                    .mt-sm-0 {
                        margin-top: 0 !important
                    }

                    .mb-sm-0 {
                        margin-bottom: 0 !important
                    }

                    .mt-sm-1 {
                        margin-top: .25rem !important
                    }

                    .mb-sm-1 {
                        margin-bottom: .25rem !important
                    }

                    .mt-sm-2 {
                        margin-top: .5rem !important
                    }

                    .mb-sm-2 {
                        margin-bottom: .5rem !important
                    }

                    .mt-sm-3 {
                        margin-top: 1rem !important
                    }

                    .mb-sm-3 {
                        margin-bottom: 1rem !important
                    }

                    .mt-sm-4 {
                        margin-top: 1.5rem !important
                    }

                    .mb-sm-4 {
                        margin-bottom: 1.5rem !important
                    }

                    .mt-sm-5 {
                        margin-top: 3rem !important
                    }

                    .mb-sm-5 {
                        margin-bottom: 3rem !important
                    }

                    .p-sm-0 {
                        padding: 0 !important
                    }

                    .pr-sm-0,
                    .px-sm-0 {
                        padding-right: 0 !important
                    }

                    .pl-sm-0,
                    .px-sm-0 {
                        padding-left: 0 !important
                    }

                    .p-sm-1 {
                        padding: .25rem !important
                    }

                    .pr-sm-1,
                    .px-sm-1 {
                        padding-right: .25rem !important
                    }

                    .pl-sm-1,
                    .px-sm-1 {
                        padding-left: .25rem !important
                    }

                    .p-sm-2 {
                        padding: .5rem !important
                    }

                    .pr-sm-2,
                    .px-sm-2 {
                        padding-right: .5rem !important
                    }

                    .pl-sm-2,
                    .px-sm-2 {
                        padding-left: .5rem !important
                    }

                    .p-sm-3 {
                        padding: 1rem !important
                    }

                    .pr-sm-3,
                    .px-sm-3 {
                        padding-right: 1rem !important
                    }

                    .pl-sm-3,
                    .px-sm-3 {
                        padding-left: 1rem !important
                    }

                    .p-sm-4 {
                        padding: 1.5rem !important
                    }

                    .pr-sm-4,
                    .px-sm-4 {
                        padding-right: 1.5rem !important
                    }

                    .pl-sm-4,
                    .px-sm-4 {
                        padding-left: 1.5rem !important
                    }

                    .p-sm-5 {
                        padding: 3rem !important
                    }

                    .pr-sm-5,
                    .px-sm-5 {
                        padding-right: 3rem !important
                    }

                    .pl-sm-5,
                    .px-sm-5 {
                        padding-left: 3rem !important
                    }
                }

                @media (min-width:768px) {
                    .mt-md-0 {
                        margin-top: 0 !important
                    }

                    .mb-md-0 {
                        margin-bottom: 0 !important
                    }

                    .mt-md-1 {
                        margin-top: .25rem !important
                    }

                    .mb-md-1 {
                        margin-bottom: .25rem !important
                    }

                    .mt-md-2 {
                        margin-top: .5rem !important
                    }

                    .mb-md-2 {
                        margin-bottom: .5rem !important
                    }

                    .mt-md-3 {
                        margin-top: 1rem !important
                    }

                    .mb-md-3 {
                        margin-bottom: 1rem !important
                    }

                    .mt-md-4 {
                        margin-top: 1.5rem !important
                    }

                    .mb-md-4 {
                        margin-bottom: 1.5rem !important
                    }

                    .mt-md-5 {
                        margin-top: 3rem !important
                    }

                    .mb-md-5 {
                        margin-bottom: 3rem !important
                    }

                    .p-md-0 {
                        padding: 0 !important
                    }

                    .pr-md-0,
                    .px-md-0 {
                        padding-right: 0 !important
                    }

                    .pl-md-0,
                    .px-md-0 {
                        padding-left: 0 !important
                    }

                    .p-md-1 {
                        padding: .25rem !important
                    }

                    .pr-md-1,
                    .px-md-1 {
                        padding-right: .25rem !important
                    }

                    .pl-md-1,
                    .px-md-1 {
                        padding-left: .25rem !important
                    }

                    .p-md-2 {
                        padding: .5rem !important
                    }

                    .pr-md-2,
                    .px-md-2 {
                        padding-right: .5rem !important
                    }

                    .pl-md-2,
                    .px-md-2 {
                        padding-left: .5rem !important
                    }

                    .p-md-3 {
                        padding: 1rem !important
                    }

                    .pr-md-3,
                    .px-md-3 {
                        padding-right: 1rem !important
                    }

                    .pl-md-3,
                    .px-md-3 {
                        padding-left: 1rem !important
                    }

                    .p-md-4 {
                        padding: 1.5rem !important
                    }

                    .pr-md-4,
                    .px-md-4 {
                        padding-right: 1.5rem !important
                    }

                    .pl-md-4,
                    .px-md-4 {
                        padding-left: 1.5rem !important
                    }

                    .p-md-5 {
                        padding: 3rem !important
                    }

                    .pr-md-5,
                    .px-md-5 {
                        padding-right: 3rem !important
                    }

                    .pl-md-5,
                    .px-md-5 {
                        padding-left: 3rem !important
                    }
                }

                @media (min-width:992px) {
                    .mt-lg-0 {
                        margin-top: 0 !important
                    }

                    .mb-lg-0 {
                        margin-bottom: 0 !important
                    }

                    .mt-lg-1 {
                        margin-top: .25rem !important
                    }

                    .mb-lg-1 {
                        margin-bottom: .25rem !important
                    }

                    .mt-lg-2 {
                        margin-top: .5rem !important
                    }

                    .mb-lg-2 {
                        margin-bottom: .5rem !important
                    }

                    .mt-lg-3 {
                        margin-top: 1rem !important
                    }

                    .mb-lg-3 {
                        margin-bottom: 1rem !important
                    }

                    .mt-lg-4 {
                        margin-top: 1.5rem !important
                    }

                    .mb-lg-4 {
                        margin-bottom: 1.5rem !important
                    }

                    .mt-lg-5 {
                        margin-top: 3rem !important
                    }

                    .mb-lg-5 {
                        margin-bottom: 3rem !important
                    }

                    .p-lg-0 {
                        padding: 0 !important
                    }

                    .pr-lg-0,
                    .px-lg-0 {
                        padding-right: 0 !important
                    }

                    .pl-lg-0,
                    .px-lg-0 {
                        padding-left: 0 !important
                    }

                    .p-lg-1 {
                        padding: .25rem !important
                    }

                    .pr-lg-1,
                    .px-lg-1 {
                        padding-right: .25rem !important
                    }

                    .pl-lg-1,
                    .px-lg-1 {
                        padding-left: .25rem !important
                    }

                    .p-lg-2 {
                        padding: .5rem !important
                    }

                    .pr-lg-2,
                    .px-lg-2 {
                        padding-right: .5rem !important
                    }

                    .pl-lg-2,
                    .px-lg-2 {
                        padding-left: .5rem !important
                    }

                    .p-lg-3 {
                        padding: 1rem !important
                    }

                    .pr-lg-3,
                    .px-lg-3 {
                        padding-right: 1rem !important
                    }

                    .pl-lg-3,
                    .px-lg-3 {
                        padding-left: 1rem !important
                    }

                    .p-lg-4 {
                        padding: 1.5rem !important
                    }

                    .pr-lg-4,
                    .px-lg-4 {
                        padding-right: 1.5rem !important
                    }

                    .pl-lg-4,
                    .px-lg-4 {
                        padding-left: 1.5rem !important
                    }

                    .p-lg-5 {
                        padding: 3rem !important
                    }

                    .pr-lg-5,
                    .px-lg-5 {
                        padding-right: 3rem !important
                    }

                    .pl-lg-5,
                    .px-lg-5 {
                        padding-left: 3rem !important
                    }
                }

                .text-justify {
                    text-align: justify !important
                }

                .text-left {
                    text-align: left !important
                }

                .text-center {
                    text-align: center !important
                }

                @media (min-width:576px) {
                    .text-sm-left {
                        text-align: left !important
                    }

                    .text-sm-center {
                        text-align: center !important
                    }
                }

                @media (min-width:768px) {
                    .text-md-left {
                        text-align: left !important
                    }

                    .text-md-center {
                        text-align: center !important
                    }
                }

                @media (min-width:992px) {
                    .text-lg-left {
                        text-align: left !important
                    }

                    .text-lg-center {
                        text-align: center !important
                    }
                }

                .text-white {
                    color: #fff !important
                }

                .text-danger {
                    color: #000000 !important
                }

                a.text-danger:focus,
                a.text-danger:hover {
                    color: #000000 !important
                }

                .text-body {
                    color: #212529 !important
                }

                .text-white-50 {
                    color: rgba(255, 255, 255, .5) !important
                }

                @media print {

                    *,
                    ::after,
                    ::before {
                        text-shadow: none !important;
                        -webkit-box-shadow: none !important;
                        box-shadow: none !important
                    }

                    a:not(.btn) {
                        text-decoration: underline
                    }

                    img {
                        page-break-inside: avoid
                    }

                    h2,
                    h3,
                    p {
                        orphans: 3;
                        widows: 3
                    }

                    h2,
                    h3 {
                        page-break-after: avoid
                    }

                    @page {
                        size: a3
                    }

                    body {
                        min-width: 992px !important
                    }

                    .container {
                        min-width: 992px !important
                    }
                }
            </style>
            <style type="text/css">
                /**
            * @license
            * Copyright Google LLC All Rights Reserved.
            *
            * Use of this source code is governed by an MIT-style license that can be
            * found in the LICENSE file at https://github.com/material-components/material-components-web/blob/master/LICENSE
            */

                @-webkit-keyframes mdc-ripple-fg-radius-in {
                    from {
                        -webkit-animation-timing-function: cubic-bezier(.4, 0, .2, 1);
                        animation-timing-function: cubic-bezier(.4, 0, .2, 1);
                        -webkit-transform: translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1);
                        transform: translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)
                    }

                    to {
                        -webkit-transform: translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1));
                        transform: translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))
                    }
                }

                @keyframes mdc-ripple-fg-radius-in {
                    from {
                        -webkit-animation-timing-function: cubic-bezier(.4, 0, .2, 1);
                        animation-timing-function: cubic-bezier(.4, 0, .2, 1);
                        -webkit-transform: translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1);
                        transform: translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)
                    }

                    to {
                        -webkit-transform: translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1));
                        transform: translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))
                    }
                }

                @-webkit-keyframes mdc-ripple-fg-opacity-in {
                    from {
                        -webkit-animation-timing-function: linear;
                        animation-timing-function: linear;
                        opacity: 0
                    }

                    to {
                        opacity: var(--mdc-ripple-fg-opacity, 0)
                    }
                }

                @keyframes mdc-ripple-fg-opacity-in {
                    from {
                        -webkit-animation-timing-function: linear;
                        animation-timing-function: linear;
                        opacity: 0
                    }

                    to {
                        opacity: var(--mdc-ripple-fg-opacity, 0)
                    }
                }

                @-webkit-keyframes mdc-ripple-fg-opacity-out {
                    from {
                        -webkit-animation-timing-function: linear;
                        animation-timing-function: linear;
                        opacity: var(--mdc-ripple-fg-opacity, 0)
                    }

                    to {
                        opacity: 0
                    }
                }

                @keyframes mdc-ripple-fg-opacity-out {
                    from {
                        -webkit-animation-timing-function: linear;
                        animation-timing-function: linear;
                        opacity: var(--mdc-ripple-fg-opacity, 0)
                    }

                    to {
                        opacity: 0
                    }
                }
            </style>
            <style type="text/css">
                @font-face {
                    font-family: "Segoe UI";
                    src: url('http://fonts.cdnfonts.com/css/segoe-ui-4');
                }

                * {
                    font-family: "Segoe UI";
                }

                /* .color-button{
                    color:#28a745;
                } */

                /* .color-primary {
                    color: #41ACBC !important;
                } */

                /* .bg-color-ascent {
                    background: #f17341 !important;
                    border-color: #f17341 !important;
                } */

                .btn-rounded {
                    border-radius: 20px;
                }
            </style>
            <script type="text/javascript">
                function getQueryStringValue(key) {
                    return decodeURIComponent(
                        window.location.search.replace(
                            new RegExp(
                                "^(?:.*[&\\?]" +
                                encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") +
                                "(?:\\=([^&]*))?)?.*$",
                                "i"
                            ),
                            "$1"
                        )
                    );
                }

                function isEmail(email) {
                    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
                    return regex.test(email);
                }
            </script>
            <!-- PLEASE SET UP URL HERE -->

            <!-- <link rel="shortcut icon" href= base_url+"/files/kemanayo_favicon.png" type="image/x-icon"> -->
        </head>
        <body>
            <div>
                <div style="margin-bottom: 8rem;">
                    <div class="shadow p-3 position-fixed bg-white w-100" style="z-index: 2; top: 0px;">
                        <div class="container">
                            <div class="row d-flex align-items-center">
                                <div class="col-12 col-md-6 text-center text-lg-left"><a href="/"><img src="" height="48rem"
                                            id="bannerImage" hidden></a></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="display: none;">
                    <div class="position-fixed w-100 h-100 d-flex align-items-center justify-content-center"
                        style="z-index: 99; top: 0px;">
                        <div class="loader"></div>
                    </div>
                </div>
                <div class="container mt-4 mb-4">
                    <div class="row">
                        <div class="col-12 text-center">
                            <div class="card shadow-sm d-inline-block" style="width: 25rem;">
                                <div class="card-body p-0 text-left">
                                    <div class="row p-3">
                                        <div class="col-12 mb-3 position-relative pl-5 pr-5">
                                            <div class="bg-color-ascent bg-danger h-100 position-absolute"
                                                style="width: 0.5rem; left: 0px; top: 0px;"></div>
                                            <h3><strong>Reset Password</strong></h3>
                                        </div>
                                        <div class="col-12 form-group pl-5 pr-5"><label for="email">Email</label><input
                                                type="text" id="user" name="user" aria-describedby="emailHelp"
                                                class="form-control" required></div>
                                        <div class="col-12 form-group pl-5 pr-5"><label for="password">New
                                                Password</label><input type="password" id="password" name="password"
                                                aria-describedby="emailHelp" class="form-control" required>
                                        </div>
                                        <div class="col-12 form-group pl-5 pr-5"><label for="password">Re-enter New
                                                Password</label><input type="password" id="re_password" name="re_password"
                                            aria-describedby="emailHelp" class="form-control" required>
                                        <label style="display:block;text-align:right;font-size: 13px;"> Please re-enter your
                                            new password </label>
                                    </div>
                                </div>
                            </div>
                            <div class="card-footer p-3 text-left">
                                <div class="row">
                                    <div class="col-12 pl-5 pr-5"><button id="submit"
                                            class="btn btn-danger w-100 bg-color-ascent btn-rounded color-button"><strong>Reset
                                                Password</strong></button></div>
                                    <div class="col-12 form-group mt-1 mb-0 pl-5 pr-5"><label for="email">Still remember
                                            your password? <a href="/#/login" class="color-primary">Login here</a></label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </div>

            <script>
                var login_site = '"""+reset_password_settings.get("login_site")+ """';
                var using_call_php = """+ str(reset_password_settings.get("using_callphp","0"))+""";
                var base_url = "";

                if (using_call_php){
                    base_url = "/api/call.php?url=";
                }
                else{
                    base_url = '"""+reset_password_settings.get("url_frappe")+"""';
                }
             
                var app_name = '"""+reset_password_settings.get("module_name")+"""';
                var imageBanner = "";
                var primaryColor = "#000000"
                var secondaryColor = "#e9e9e9"
                var fontColorDefault = "#000000"
                var fontColorButton = "#e9e9e9"

                $.ajax({
                    method: "GET",
                    url: base_url + "/api/method/" + app_name +
                        ".user_integration.api.api_reset_password.get_style_reset_password",
                    async: false,
                    dataType: "json",
                    contentType: "application/json",
                    processData: false,
                    success: function (data) {
                        if (data["message"]["data"]["banner_image"]) {
                            imageBanner = String(base_url + data["message"]["data"]["banner_image"])
                        }
                        if (data["message"]["data"]["color_primary"]) {
                            primaryColor = String(data["message"]["data"]["color_primary"])
                        }
                        if (data["message"]["data"]["color_secondary"]) {
                            secondaryColor = String(data["message"]["data"]["color_secondary"])
                        }
                        if (data["message"]["data"]["font_color_default"]) {
                            fontColorDefault = String(data["message"]["data"]["font_color_default"])
                        }
                        if (data["message"]["data"]["font_color_button"]) {
                            fontColorButton = String(data["message"]["data"]["font_color_button"])
                        }
                        console.log(imageBanner);
                        console.log(data)
                        // document.getElementById("bannerImage").src = "/files/logo.png";
                        setTimeout(function () {
                            $("#bannerImage").attr('src', imageBanner);
                            $("#bannerImage").removeAttr('hidden');
                        }, 0);

                        setTimeout(function () {
                            $("<style>.bg-color-ascent { background: " + primaryColor +
                                    " !important; border-color: " + primaryColor + " !important;} </style>")
                                .appendTo("head")
                            $("<style>.color-primary {color: " + secondaryColor +
                                " !important;} */</style>").appendTo("head")
                            $("<style> body {margin: 0;font-size: 1rem;font-weight: 400;line-height: 1.5;color: " +
                                    fontColorDefault + ";text-align: left;background-color: #fff} </style>")
                                .appendTo("head")
                            $("<style>.color-button {color: " + fontColorButton +
                                " !important;} */</style>").appendTo("head")
                        }, 0);
                    },
                    complete: function () {


                    },
                    error: function (e) {
                        Alert("Reset password can't load the style data. Please contact administrator")
                    }

                });

                if (!using_call_php){
                    $.get(base_url + "/api/method/" + app_name +
                            ".user_integration.api.api_reset_password.is_login")
                        .done(function (data) {
                            console.log(data)
                            if (data.message != "Guest") {
                                Swal.fire({
                                    position: 'center',
                                    type: 'info',
                                    title: 'Oops, you already sign in as ' + data.message + '.'
                                })
                            }
                        });

                    }


                $("#submit").on("click", function () {
                    var json = {};
                    json["user"] = $("#user").val() || ""
                    json["password"] = $("#password").val() || ""
                    json["re_password"] = $("#re_password").val() || ""
                    json["key"] = getQueryStringValue("key")
                    console.log(json)
                    if (!isEmail(json["user"])) {
                        return Swal.fire({
                            type: 'error',
                            title: "Email error",
                            text: "Please check again your email, make sure it filled and in the right format.",
                        })
                    }
                    if (!json["password"]) {
                        return Swal.fire({
                            type: 'error',
                            title: "New Password must be filled",
                            text: "Please fill your new password",
                        })
                    }
                    if (json["re_password"] != json["password"]) {
                        return Swal.fire({
                            type: 'error',
                            title: "Your new password and confirmation new password don't match",
                            text: "Please check again your new password and confirmation new password, make them same.",
                        })
                    }
                    $.ajax({
                        method: "POST",
                        url: base_url + "/api/method/" + app_name +
                            ".user_integration.api.api_reset_password.reset_password",
                        async: false,

                        data: JSON.stringify(json),
                        dataType: "json",
                        contentType: "application/json",
                        processData: false,
                        success: function (data) {
                            console.log(data)
                            if (data.message.code == 200) {
                                Swal.fire({
                                    type: 'success',
                                    title: "Success",
                                    text: 'Your password has been changed',
                                }).then((result) => {
                                    window.location =
                                        "/#";
                                })


                            } else {
                                Swal.fire({
                                    type: 'error',
                                    title: "Can't reset your password",
                                    text: data.message.error,
                                })
                            }


                        },
                        error: function (e) {
                            console.log(e);
                            var err;
                            if (e.responseJSON._server_messages != null) {
                                err = JSON.parse(e.responseJSON
                                    ._server_messages);
                                err = JSON.parse(err[0]);
                                err = err["message"];
                                console.log(err)
                                Swal.fire({
                                    position: 'center',
                                    type: 'error',
                                    title: 'Oops, something wrong. Please contact us.',
                                    text: err,

                                })
                            } else {
                                Swal.fire({
                                    position: 'center',
                                    type: 'error',
                                    title: 'Oops, server Error. Please contact us.'
                                })
                            }
                        }

                    });
                });
            </script>
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@8"></script>
        </body>

    </html>"""
        return reset_password_html

