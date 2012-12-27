//--------------------------------------------------
// PLUGIN VARIABLES
//--------------------------------------------------
var JQUERY_VERSION = '1.6.1';
var DOMAIN = 'http://activebuys.com';
var SLIDETIME = 300;
var AUTO_SLIDE;

//--------------------------------------------------
// SLIDE SHOW
//--------------------------------------------------
function activeBuysSlide(slideId) {
    var slideWidth = jQuery('div#ab-widget ul.ab-deals').width();

    if ( !jQuery('div#ab-widget').hasClass('ab-animating') ) {
        jQuery('div#ab-widget').addClass('ab-animating');

        var active = jQuery('div#ab-widget li.ab-deal.ab-active');
        var next = jQuery('div#ab-widget li#ab-s-' + slideId);
        var activeDir = '-';
        var nextDir = '';

        if ( !next.prevAll('li.ab-deal').hasClass('ab-active') ) {
            activeDir = '';
            nextDir = '-';
        }

        jQuery('div#ab-widget div.ab-slide-nav a.ab-active').removeClass('ab-active');
        jQuery('div#ab-widget a#ab-n-' + slideId).addClass('ab-active');

        active.animate({ left:  activeDir + slideWidth + 'px' }, SLIDETIME, function() {
			jQuery(this).removeClass('ab-active');
		});
		next.css('left', nextDir + slideWidth + 'px').addClass('ab-next').animate({ left:  '0px' }, SLIDETIME, function() {
			jQuery(this).removeClass('ab-next').addClass('ab-active');
			jQuery('div#ab-widget').removeClass('ab-animating');
		});
    }
}

function activeBuysSlideshow() {
    jQuery('div#ab-widget li.ab-deal').each( function(i) {
        var newI = i + 1;

        jQuery(this).attr('id', 'ab-s-' + newI);
        jQuery('div#ab-widget div.ab-slide-nav').append('<a id="ab-n-' + newI + '" class="ab-slide-link ab-hide-text" href="#/' + newI + '/">' + newI + '</a>');
    });

    jQuery('div#ab-widget li.ab-deal:first, div#ab-widget div.ab-slide-nav a:first').addClass('ab-active');

    jQuery('div#ab-widget a.ab-slide-prev').click( function (e) {
        e.preventDefault();
        jQuery(this).blur();
        window.clearInterval(AUTO_SLIDE);
        var slideId = 0;

        if ( !jQuery(this).hasClass('ab-active') ) {
            var active = jQuery('div#ab-widget li.ab-deal.ab-active');

            if ( active.is(':first-child') ) {
                slideId = jQuery('div#ab-widget li.ab-deal:last').attr('id').replace('ab-s-', '');
            } else {
                slideId = active.prev().attr('id').replace('ab-s-', '');
            }

            activeBuysSlide(slideId);
        }
    });

    jQuery('div#ab-widget a.ab-slide-next').click( function (e) {
        e.preventDefault();
        jQuery(this).blur();
        window.clearInterval(AUTO_SLIDE);

        nextButton();
    });

    jQuery('div#ab-widget div.ab-slide-nav a').click( function (e) {
        e.preventDefault();
        jQuery(this).blur();
        window.clearInterval(AUTO_SLIDE);

        if ( !jQuery(this).hasClass('ab-active') ) {
            var slideId = jQuery(this).attr('id').replace('ab-n-', '');

            activeBuysSlide(slideId);
        }
   });

   // Auto slide images
   AUTO_SLIDE = setInterval("nextButton()", 5000);
}

function nextButton() {
    if ( !jQuery('div#ab-widget a.ab-slide-next').hasClass('ab-active') ) {
        var active = jQuery('div#ab-widget li.ab-deal.ab-active');
        var slideId = 0;

        if ( active.is(':last-child') ) {
            slideId = jQuery('div#ab-widget li.ab-deal:first').attr('id').replace('ab-s-', '');
        } else {
            slideId = active.next().attr('id').replace('ab-s-', '');
        }

        activeBuysSlide(slideId);
    }
}

//--------------------------------------------------
// DISPLAY THE WIDGET
//--------------------------------------------------
function displayActiveBuysWidget(APIKEY, size, link_color, hover_color) {
    CSSURL = new String();
    CSSURL = DOMAIN + '/static/widget/style' + size + '.css';
    APIURL = DOMAIN + '/widgets/widget?api=' + APIKEY + '&callback=?';

    //var ab01 = jQuery.noConflict(true);
    jQuery('head').append('<link rel="stylesheet" href="' + CSSURL + '" type="text/css" media="all" />');
    jQuery('head').append('<style type="text/css">#ab-widget a { color: ' + link_color + '; text-decoration: none; }#ab-widget a:hover { color: ' + hover_color + '; }</style>');
    jQuery('#active-buys-widget').replaceWith('<div id="ab-widget"><div class="ab-loading"></div></div>');
    var widgetElement = document.getElementById("ab-widget");
    if (widgetElement !== null) {
        jQuery.getJSON(APIURL, function(data) {
            jQuery("#ab-widget").html('<h2 class="ab-logo"><a class="ab-hide-text" href="' + DOMAIN + '">ACTIVEBUYS</a></h2>');
            jQuery("#ab-widget").append('<ul class="ab-menu ab-point-12-16 ab-align-center ab-uppercase">\
        		                            <li class="ab-first"><span class="ab-active">Deals</span></li>\
        		                            <li><a href="http://blog.activebuys.com/" target="_blank">Blog</a></li>\
        		                            <li class="ab-last"><a href="http://blog.activebuys.com/?page_id=351" target="_blank">Events</a></li></ul>\
        		                            <ul class="ab-deals"></ul>\
        		                            <a class="ab-slide-prev ab-hide-text" href="#/prev/">Prev</a>\
        	                                <a class="ab-slide-next ab-hide-text" href="#/next/">Next</a>\
        			                        <div class="ab-slide-nav ab-align-center"></div>\
        	                                <a class="ab-main-link ab-point-8-10 ab-align-center" href="http://activebuys.com/" target="_blank">ACTIVEBUYS.com</a>');
            for (i = 0; i < data.length; i++) {
                ///console.log(data[i]);
                var html = '<li class="ab-deal">\
                            <h3 class="ab-title ab-bold ab-point-12-16">' + data[i].fields.title + '</h3>\
    				        <a class="ab-bold ab-point-10-16 ab-uppercase" href="' + DOMAIN + '/deals/' + data[i].fields.slug + '/?wid=' + APIKEY + '" target="_blank">View This Deal</a>\
    				        <a class="ab-hero" href="' + DOMAIN + '/deals/' + data[i].fields.slug + '/?wid=' + APIKEY + '" target="_blank">\
    				            <img src="' + data[i].extras.first_image + '" alt="image ' + i + '" />\
    				        </a>\
    			        </li>'
    			jQuery("#ab-widget ul.ab-deals").append(html);
            }
            activeBuysSlideshow();
        });
    } else {
        setTimeout("activeBuysInit()", 200);
    }
}


//--------------------------------------------------
// INITIALIZE WITH OPTIONS
//--------------------------------------------------
function activeBuysInit() {
    if (typeof(_abwparam) != 'undefined') { // parameters should be passed
        displayActiveBuysWidget(_abwparam['APIKEY'], '', _abwparam['link_color'], _abwparam['hover_color'] );
    }
}


//--------------------------------------------------
// LOAD WIDGET
//--------------------------------------------------
activeBuysLoad = function() {
    activeBuysLoad.getScript('http://ajax.googleapis.com/ajax/libs/jquery/' + JQUERY_VERSION + '/jquery.min.js');
    activeBuysLoad.tryReady(0);  // Wait until jQuery loads before we use it.
};

activeBuysLoad.getScript = function(filename) {
    var script = document.createElement('script');
    script.setAttribute('type', 'text/javascript');
    script.setAttribute('src', filename);
    if (typeof script != "undefined") {
        document.getElementsByTagName("head")[0].appendChild(script);
    }
};

activeBuysLoad.tryReady = function(time_elapsed) {
    // Poll to see if jQuery is ready
    if (typeof(jQuery) == "undefined") { // jQuery isn't loaded yet
        if (time_elapsed <= 10000) { // don't giveup for 10 seconds
            setTimeout("activeBuysLoad.tryReady(" + (time_elapsed + 200) + ")", 200);
        } else {
            // console.log("Timed out trying to load jQuery");
        }
    } else {
        // Success!
        activeBuysInit();
    }
};

if ( typeof(jQuery) == "undefined" ) { // TODO: research a better way for collision detection || jQuery.fn.jquery !== JQUERY_VERSION ) {
    // jQuery isn't loaded...go get it!
    activeBuysLoad();
} else {
	activeBuysInit();
}

