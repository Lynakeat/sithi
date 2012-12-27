if (typeof(storedomain) == 'undefined') {
    var storedomain = 'secure.activebuys.com';
}
if (typeof(sitedomain) == 'undefined') {
    var sitedomain = 'activebuys.com';
}

// foxycart.raw.2.js, compressed. Standalone file available at http://admin.foxycart.com/v/0.7.0/js/foxycart.2.js
window.jQuery||alert("This page does not have jQuery loaded. Please add jQuery to your website to ensure FoxyCart functions properly. If you are a customer seeing this alert please notify the owner of this website about it.");var FC=FC||{};FC.json={};FC.session_id="";FC.session_name="fcsid";var cookiepath=cookiepath||"";FC.client=function(a,b,c){this.storedomain=a;this.sitedomain=b.replace(/https?:\/\//i,"").replace(/www\./i,"").replace(/\/.*$/,"");this.cookiepath=c||""};
FC.client.prototype.session_initialized=!1;
FC.client.prototype.session_get=function(){if(FC.session_id!="")return this.session_initialized=!0,"&"+FC.session_name+"="+FC.session_id;this.regex=RegExp("#"+FC.session_name+"=([A-Za-z0-9]*)");if(this.regex.test(window.location.href)){var a=this.regex.exec(window.location.href);FC.session_id=a[1];this.session_set(FC.session_name,FC.session_id)}else if(document.cookie.indexOf(FC.session_name+"=")>-1){if(a=document.cookie.indexOf(FC.session_name+"="),a!=-1){var a=a+FC.session_name.length+1,b=document.cookie.indexOf(";",
a);if(b==-1)b=document.cookie.length;FC.session_id=unescape(document.cookie.substring(a,b))}}else if(FC.json.length>0)FC.session_id=FC.json.session_id,this.session_set(FC.session_name,FC.session_id);return FC.session_id!=""?(this.session_initialized=!0,"&"+FC.session_name+"="+FC.session_id):""};
FC.client.prototype.session_set=function(){var a=this.sitedomain.split(".");a[0]=="www"&&a.shift();for(var b=window.location.href.split("/"),b=b[2].split("."),a=b.length-a.length;a>0;)b.shift(),a--;b="."+b.join(".");if(b==".foxycart.com")return!1;document.cookie=FC.session_name+"="+escape(FC.session_id)+";path=/"+this.cookiepath+";domain="+b;return!0};
FC.client.prototype.session_apply=function(){var a=this;jQuery("body").delegate('a[href*="'+this.storedomain+'"]',"click",function(){RegExp(FC.session_name+"=([A-Za-z0-9]*)").test(jQuery(this).attr("href"))||jQuery(this).attr("href",jQuery(this).attr("href")+a.session_get());return a.cart_submit(this,a.cart_prepare_element(this))});jQuery("body").delegate('form[action*="'+this.storedomain+'"]',"submit",function(){jQuery(this).children("input[name="+FC.session_name+"]").length==0&&jQuery(this).prepend('<input type="hidden" name="'+
FC.session_name+'" value="'+FC.session_id+'">');return a.cart_submit(this,a.cart_prepare_element(this))})};
FC.client.prototype.cart_update=function(){var a=this;jQuery.getJSON("https://"+this.storedomain+"/cart.php?cart=get&output=json"+this.session_get()+"&callback=?",function(b){FC.json=b;if(!a.session_initialized==!0)a.session_initialized=!0,FC.session_id=b.session_id,a.session_set(),a.session_get();FC.json.product_count>0?jQuery("#fc_minicart, .fc_minicart").show():jQuery("#fc_minicart, .fc_minicart").css("display","none");jQuery("#fc_quantity, .fc_quantity").html(""+FC.json.product_count);jQuery("#fc_total_price, .fc_total_price").html(""+
a._currency_format(FC.json.total_price))})};FC.client.prototype.cart_submit=function(a,b){if(this.events.cart.preprocess.execute(a,b)==!1)return!1;return this.events.cart.process.funcs.length==0?!0:this.events.cart.process.execute(a,b)};FC.client.prototype.cart_prepare_element=function(a){var b="";a.tagName=="A"?(b=a.href.match(/\?(.*)$/),b=b[1]):a.tagName=="FORM"&&(b=jQuery(a).serialize());b.replace(/\|\|[A-Za-z0-9]{64}(\|\|open)?/g,"");return this._unserialize(b)};
FC.client.event=function(){this.funcs=[]};FC.client.event.prototype.add=function(a){typeof a!="function"&&(a=new Function(a));this.funcs.push(a)};FC.client.event.prototype.add_pre=function(a){typeof a!="function"&&(a=new Function(a));this.funcs.unshift(a)};FC.client.event.prototype.execute=function(a,b){for(var c=!0,d=0;d<this.funcs.length;d++)if(this.funcs[d](a,b)==!1)d=this.funcs.length,c=!1;return c};FC.client.prototype.events={cart:[]};
FC.client.prototype._unserialize=function(a){var a=a.split("&"),b=[];jQuery.each(a,function(){var a=this.split("=");b[a[0]]=a[1]});return b};FC.client.prototype._currency_format=function(a){a=parseFloat(a);isNaN(a)&&(a=0);var b="";a<0&&(b="-");a=Math.abs(a);a=parseInt((a+0.005)*100);a/=100;s=new String(a);s.indexOf(".")<0&&(s+=".00");s.indexOf(".")==s.length-2&&(s+="0");return s=b+s};FC.client.prototype.init=function(){this.session_apply();this.cart_update()};



// Initialize the fcc object
var fcc = new FC.client(storedomain, sitedomain, cookiepath);
fcc.events.cart.preprocess = new FC.client.event();
fcc.events.cart.process = new FC.client.event();
fcc.events.cart.postprocess = new FC.client.event();
jQuery(document).ready(function(){
    fcc.init();
});



// COLORBOX
var colorbox_width = colorbox_width || "700px";
var colorbox_height = colorbox_height || "450px";
var colorbox_close = colorbox_close || '<span>&laquo;</span> Continue Shopping';
fcc.events.cart.postprocess.add(function(e){
    fcc.cart_update();
});
fcc.events.cart.process.add(function(e){
    var href = '';
    if (e.tagName == 'A') {
        href = e.href;
    } else if (e.tagName == 'FORM') {
        href = 'https://'+storedomain+'/cart?'+jQuery(e).serialize();
    }
    if (href.match("cart=(checkout|updateinfo)") || href.match("redirect=")) {
        return true;
    } else {
        jQuery.colorbox({
            href: href,
            iframe: true,
            width: colorbox_width,
            height: colorbox_height,
            close: colorbox_close,
            onClosed: function(){fcc.events.cart.postprocess.execute(e);}
        });
        return false;
    }
});
