/*
    Get company locations for deal page.
    On changing company field, locations will be populated from company addresses
*/

function populateLocations(company_id){
    django.jQuery.getJSON('/admin/companies/company/addressajaxlist/', 
        {'id': company_id}, 
        function(data){
            // Add new items
            for (i in data.items){
                if (django.jQuery('#id_locations option[value="'+i+'"]').length == 0){
                    django.jQuery('#id_locations').append('<option value="'+i+'">'+data.items[i]+'</option>');
                }
            }
            /* 
                If locations was selected and user select same company, 
                selection will doesn't disappear from options
                If different company was selected, 
                selection will disappear, and new options would be available for selection
            */
            django.jQuery('#id_locations option').each(function(){
                if (!(django.jQuery(this).attr('value') in data.items)){
                    django.jQuery(this).remove();
                }
            })
            
            django.jQuery('#id_locations option:first').attr('selected', 'selected');

        });
}

dismissRelatedLookupPopup = function(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
    win.close();
    populateLocations(document.getElementById(name).value);
}

django.jQuery(document).ready(function($){
    if ($('#id_company').val() != ''){
        populateLocations($('#id_company').val());
    }
})
