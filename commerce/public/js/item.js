var hideTheButtonWrapper = $('*[data-fieldname="attributes"]');

frappe.ui.form.on('Item', {
    refresh: function (frm) {
        cur_frm.events.filter_uom();
        if (frm.doc.variant_of) {
            frm.set_df_property("popular", "hidden", 1)
            frm.set_df_property("new_arrival", "hidden", 1)
        }
        cur_frm.events.show_html_description()
        // if (cur_frm.is_new()){
        //     if (!cur_frm.doc.brand){
        //         cur_frm.set_value("brand","Others");
        //     }
        // }
    },
    attributes_remove: function (frm) {
        // alert("asfd");
    },
    filter_uom: function (frm) {
        cur_frm.set_query("weight_uom", function () {
            return {
                "filters": [
                    ['UOM', 'uom_name', 'in', "Kilogram,Gram"]

                ]
            }
        });
    },
    show_html_description:function(){
        cur_frm.set_df_property("description_html","options", cur_frm.doc.description_content
        );
    }
    
})