//--------------------------------------------------
// PLUGIN VARIABLES
//--------------------------------------------------
var ab01jQueryVersion = '1.6.1';
var ab01CssUrl = 'http://activebuys.com/static/widget/style.css';
var ab01WidgetUrl = 'http://activebuys.com/widget/';
var ab01SlideTime = 300;


//--------------------------------------------------
// TESTING
//--------------------------------------------------
var currentHost = document.location.hostname;

if ( currentHost == 'localhost' ) {
    var ab01CssUrl = 'http://localhost:8000/static/widget/style.css';
    var ab01WidgetUrl = 'http://localhost:8000/widget/';
} else if ( currentHost == 'mac.local' ) {
    var ab01CssUrl = 'http://mac.local:8000/static/widget/style.css';
    var ab01WidgetUrl = 'http://mac.local:8000/widget/';
}

//--------------------------------------------------
// SLIDE SHOW
//--------------------------------------------------
function ab01Slide(slideId) {
    var slideWidth = ab01('div#ab-widget-01 ul.ab-deals').width();
    
    if ( !ab01('div#ab-widget-01').hasClass('ab-animating') ) {
        ab01('div#ab-widget-01').addClass('ab-animating');
        
        var active = ab01('div#ab-widget-01 li.ab-deal.ab-active');
        var next = ab01('div#ab-widget-01 li#ab-01-s-' + slideId);
        var activeDir = '-';
        var nextDir = '';
        
        if ( !next.prevAll('li.ab-deal').hasClass('ab-active') ) {
            var activeDir = '';
            var nextDir = '-';
        }
        
        ab01('div#ab-widget-01 div.ab-slide-nav a.ab-active').removeClass('ab-active');
        ab01('div#ab-widget-01 a#ab-01-n-' + slideId).addClass('ab-active');
        
        active.animate({ left:  activeDir + slideWidth + 'px' }, ab01SlideTime, function() {
			ab01(this).removeClass('ab-active');
		});
		next.css('left', nextDir + slideWidth + 'px').addClass('ab-next').animate({ left:  '0px' }, ab01SlideTime, function() {
			ab01(this).removeClass('ab-next').addClass('ab-active');
			ab01('div#ab-widget-01').removeClass('ab-animating');
		});
    }
}

function ab01Slideshow() {
    ab01('div#ab-widget-01 li.ab-deal').each( function(i) {
        var newI = i + 1;
        
        ab01(this).attr('id', 'ab-01-s-' + newI);
        ab01('div#ab-widget-01 div.ab-slide-nav').append('<a id="ab-01-n-' + newI + '" class="ab-slide-link ab-hide-text" href="#/' + newI + '/">' + newI + '</a>');
    });
    
    ab01('div#ab-widget-01 li.ab-deal:first, div#ab-widget-01 div.ab-slide-nav a:first').addClass('ab-active');
    
    ab01('div#ab-widget-01 a.ab-slide-prev').click( function (e) {
        e.preventDefault();
        ab01(this).blur();
        
        if ( !ab01(this).hasClass('ab-active') ) {
            var active = ab01('div#ab-widget-01 li.ab-deal.ab-active');
         
            if ( active.is(':first-child') ) {
                var slideId = ab01('div#ab-widget-01 li.ab-deal:last').attr('id').replace('ab-01-s-', '');
            } else {
                var slideId = active.prev().attr('id').replace('ab-01-s-', '');
            }
        
            ab01Slide(slideId);
        }
    });
    
    ab01('div#ab-widget-01 a.ab-slide-next').click( function (e) {
        e.preventDefault();
        ab01(this).blur();
        
        if ( !ab01(this).hasClass('ab-active') ) {
            var active = ab01('div#ab-widget-01 li.ab-deal.ab-active');
         
            if ( active.is(':last-child') ) {
                var slideId = ab01('div#ab-widget-01 li.ab-deal:first').attr('id').replace('ab-01-s-', '');
            } else {
                var slideId = active.next().attr('id').replace('ab-01-s-', '');
            }
        
            ab01Slide(slideId);
        }
    });

    ab01('div#ab-widget-01 div.ab-slide-nav a').click( function (e) {
        e.preventDefault();
        ab01(this).blur();
        
        if ( !ab01(this).hasClass('ab-active') ) {
            var slideId = ab01(this).attr('id').replace('ab-01-n-', '');
            
            ab01Slide(slideId);
        }
   });
}


//--------------------------------------------------
// LOAD WIDGET
//--------------------------------------------------
function ab01Load() {
    ab01 = jQuery.noConflict();
    
    ab01('head').append('<link rel="stylesheet" href="' + ab01CssUrl + '" type="text/css" media="all" />');
    ab01('a#active-buys-widget').replaceWith('<div id="ab-widget-01"><div class="ab-loading"></div></div>');
    ab01('div#ab-widget-01').load(ab01WidgetUrl + ' div.widget-content', function() {
        ab01Slideshow();
    });
}


//--------------------------------------------------
// LOAD WIDGET
//--------------------------------------------------
if ( typeof jQuery === "undefined" || jQuery.fn.jquery !== ab01jQueryVersion ) {
    var newJQuerySrc = document.createElement('script');
    newJQuerySrc.setAttribute('type', 'text/javascript');
    newJQuerySrc.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/' + ab01jQueryVersion + '/jquery.min.js')
    newJQuerySrc.onload = function() { // Run js once jQuery and document have loaded
        ab01Load();
    };
    newJQuerySrc.onreadystatechange = function() { // Same thing but for IE
	    if ( this.readyState == 'complete' || this.readyState == 'loaded' ) {
	        ab01Load();
        }
    }
    
    document.getElementsByTagName('head')[0].appendChild(newJQuerySrc);
} else {
	ab01Load();
}

