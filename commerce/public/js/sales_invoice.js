frappe.ui.form.on('Sales Invoice', {
    refresh: function (frm) {
        cur_frm.events.hide_shipping_info_before_shipping();

        // Add custom button
        frm.add_custom_button(__("Create Delivery Tracking"), function () {

            frappe.model.open_mapped_doc({
                method: "commerce.custom_form.sales_invoice.create_form_delivery_tracking",
                frm: cur_frm
            })

        }, "Delivery Tracking");

        frm.add_custom_button(__("View Delivery Tracking"), function () {
            if (cur_frm.doc.name) {
                window.open("/desk#List/Delivery%20Tracking/List?external_id="+cur_frm.doc.name)
            }
        }, "Delivery Tracking");
    },
    use_internal_shipping:function(frm){
        if(cur_frm.doc.use_internal_shipping == 1){
            cur_frm.set_df_property("delivery_receipt","read_only",1)
            cur_frm.set_df_property("internal_shipping","reqd",1)
        }   
        else if (cur_frm.doc.use_internal_shipping == 0 ){
            cur_frm.set_df_property("delivery_receipt","read_only",0)
            cur_frm.set_df_property("internal_shipping","reqd",0)

        }
    },
    shipping_status:function(frm){
        cur_frm.events.hide_shipping_info_before_shipping();

    },
    hide_shipping_info_before_shipping:function(){
        if (cur_frm.doc.shipping_status == "Pending" || cur_frm.doc.shipping_status == "Packaged" ){
            cur_frm.set_df_property("use_internal_shipping","read_only",1);
            cur_frm.set_df_property("internal_shipping","read_only",1);
            cur_frm.set_df_property("delivery_receipt","read_only",1);
        }else{
            cur_frm.set_df_property("use_internal_shipping","read_only",0);
            cur_frm.set_df_property("internal_shipping","read_only",0);
            cur_frm.set_df_property("delivery_receipt","read_only",0);
        }
    }
})