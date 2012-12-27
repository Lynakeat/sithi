function mycarousel_initCallback(carousel) {
    $('a.slider-next').bind('click', function() {
        carousel.next();
        return false;
    });
    $('a.slider-prev').bind('click', function() {
        carousel.prev();
        return false;
    });
};

$(function(){
	$(".min-slider").jcarousel({
	    scroll: 1,
	    wrap: 'both',
	    initCallback: mycarousel_initCallback,
	    buttonNextHTML: null,
	    buttonPrevHTML: null
	}); 
	
	$('.blink').focus(function () {
		if ($(this).val() == $(this).attr('title')) {
			$(this).val('');
		}
	});
	
	$('.blink').blur(function () {
		if ($(this).val() == '') {
			$(this).val($(this).attr('title'));
		}
	});
	
	$('.label-blink').focus(function () {
		$(this).parents('.fieldset').find('label').fadeOut();
	});
	
	$('.label-blink').blur(function () {
		if ($(this).val() == '') {
			$(this).parents('.fieldset').find('label').fadeIn();
		}
	});
	
	$('.comments-form input').focus(function(){
		$(this).parents('span').addClass('active-field');
	});
	$('.comments-form input').blur(function(){
		$(this).parents('span').removeClass('active-field');
	});
	
	if($.browser.msie && $.browser.version==6)
	{
		DD_belatedPNG.fix('.box-t, .box-c, .box-b, a.buy-now-btn, .min-slider a.slider-prev, .min-slider a.slider-next, .services ul li, .imgs-section, a.back-arr, a.cancel-btn, .featured ul li, .tooltip-t, .tooltip-b, .tooltip-c');
	}
	
    /* expand long text */
    $('div.expandable').expander({
        slicePoint:       150,  // default is 100
        summaryClass: 'expander-summary',
        detailClass: 'expander-details'
        // expandPrefix:     ' ', // default is '... '
        // expandText:       '[...]', // default is 'read more'
        // collapseTimer:    5000, // re-collapses after 5 seconds; default is 0, so no re-collapsing
        // userCollapseText: '[^]'  // default is 'read less'
      });

	/* expandable list */
	$('.exp-list h3 a').click(function(){
		$(this).parents('h3').toggleClass('exp');
		$(this).parents('h3').next('.entry').slideToggle();
		$('html,body').animate({
            scrollTop: $(this).offset().top - 30}, 'slow');
		return false;
	});
	
	/* colorbox popups */
	$('a.pop-loader').click(function(){
        $.colorbox({
            href: $(this).attr('href'),
    		onComplete: function(){
	    		if($.browser.msie && $.browser.version==6){DD_belatedPNG.fix('#cboxClose');}
		    }
        })
        return false;
    })
    $('a.pop-loader-iframe').click(function(){
        $.colorbox({
            href: $(this).attr('href'),
            iframe: true,
            innerWidth: "680px",
            innerHeight: "400px",
            onComplete: function(){
                if($.browser.msie && $.browser.version==6){DD_belatedPNG.fix('#cboxClose');}
            }
        })
        return false;
    })
    $('a.pop-loader-inline').click(function(){
        $.colorbox({
            href: $(this).attr('href'),
            inline: true,
            onComplete: function(){
                if($.browser.msie && $.browser.version==6){DD_belatedPNG.fix('#cboxClose');}
            }
        })
        return false;
    })
	
	$('span.field input').focus(function(){
		$(this).parents('span').addClass('active');
	});
	$('span.field input').blur(function(){
		$(this).parents('span').removeClass('active');
	});
	
	$('span.textarea-field textarea').focus(function(){
		$(this).parents('span').addClass('active');
	});
	$('span.textarea-field textarea').blur(function(){
		$(this).parents('span').removeClass('active');
	});

	/* account edit functions */
	$('.account-info .row a').click(function(){
		var obj = $(this).parents('.row');
		var text = obj.find('span.data').text();
		
		$('.account-info .row').each(function(){
			if($(this).find('.edit-row').is(':visible')){
				$('.edit-row', $(this)).slideUp();
				$('.view', $(this)).slideDown();
			}
		});
	
		if(!obj.find('input.input').hasClass('pass'))
			obj.find('input.input').val(text);
			
		$('.view', obj).slideUp();
		$('.edit-row', obj).slideDown();
		
		return false;
	});
	
	var error = 0;

    if ($('.account-info .row input.row-submit').length > 0){
    $('.account-info .row input.row-submit').parent().ajaxForm({
        dataType: 'json',
        success: function(data, statusText, xhr, $form){
            var obj = $form.parents('.row');
            var result = "";
            
            if($('input.input', obj).hasClass('pass')){
                result = "••••••••";
            } else{
                result = $('input.input', obj).val();
            }
           
            /*
            if($('ul', obj).length){
                result = "";
                $('ul li', obj).each(function(){
                    if($(this).find('input:radio[checked]').length > 0){
                        result = $(this).find('input:radio[checked]').parent('label').text();
                    }
                });
            }
            */

    		if($('ul', obj).length){
	    		result = "";
		    	$('ul li', obj).each(function(){
			    	if($(this).find('input.check').is(':checked')){
					    result += $(this).find('label').text()+"<br/>";
    				}
	    		});
		    }

    		if(data.success){
	    		$('span.data', obj).html(result);
		    	$('.edit-row', obj).slideUp();
			    $('.view', obj).slideDown();
                $('em', obj).remove();
    		} else {
                $('.field', obj).addClass('error-field');
                $('.field em', obj).remove();
                for (i in data.messages){
                    $('.field', obj).append('<em>'+data.messages[i]+'</em>')
                }
            }
        }
    })
    }// if -->
	
	reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
	
	$('input#account-mail').keyup(function(){
		if(reg.test($(this).val()) == false){
			$(this).parents('.edit-row').find('p.account-error').slideDown();
			error = 1;
		} else {
			$(this).parents('.edit-row').find('p.account-error').slideUp();
			error = 0;
		}
	})


    if ($('#contacts-form').length > 0){
    	$('#contacts-form').ajaxForm({
            dataType: 'json',
            success: function(data,s,x,$form){
                if (data.success){
                    $form.fadeOut(function(){
                        $form.parent().find('.thankyou-txt').fadeIn();
                    })
                } else {
                    $('input').parent().removeClass('error-field');
                    $('em').remove();
                    for (i in data.messages){
                        $('#id_'+i).parent().addClass('error-field');
                        $('#id_'+i).after('<em>'+data.messages[i]+'</em>');
                    }
                }
            }
        });
    }
	
	/* change from txt to pass input */
	$('input.true-pass').hide();
	$('input.fake-pass').focus(function(){
		$(this).hide();
		$(this).next('input').show().focus();
		$(this).parents('span.field').addClass('active');
	});
	
	$('input.true-pass').blur(function(){
		if($(this).val()==""){
			$(this).hide();
			$(this).prev('input').show().val($(this).prev('input').attr('title'));
		}
		$(this).parents('span.field').removeClass('active');
	});
	
	/* login show hide functions */
	$('a.login-option-select').click(function(){
		var target = $($(this).attr('href'));
		$('.main-login-option').fadeOut(function(){
			target.fadeIn();
		});
		return false
	});
	
	$(".custom-check").dgStyle();

    // show gift form 
    var toggle_gift_form = function(result){
		if(result=='True'){
			$('.gift-hidden').show();
		} else {
			$('.gift-hidden').hide();
		}
    }
    toggle_gift_form($('.gift-option[checked]').val());
    $('input.gift-option').change(function(){
        toggle_gift_form($(this).val());
	});
	
    // surprise fields 
    var toggle_surprise_fields = function(el){
        var result = $(el).val();
		if(result=='False'){
			$(el).parents('.radios').find('span.field').show();
		} else {
			$(el).parents('.radios').find('span.field').hide();
		}
    }
    toggle_surprise_fields($('.radio[name="surprise"][checked]'));
	$('.option input.radio').change(function(){
		toggle_surprise_fields($(this));
	});

    // purshes history filter 
    $('select.purchase-history-list').change(function(){
        var val = $(this).val();
        if (val == 'entry'){
            $('.entry').show();
        } else {
            $('.entry').hide();
            $('.'+val).show();
        }
    })
	
	/* FOXY HARD CODE */
	$('#fc_cart_head_quantity').text('QTY');
	$('#fc_complete_order_button').text('Check Out Now')
	
	$('input.fc_text').focus(function(){
		$(this).addClass('fc_active');
	});
	$('input.fc_text').blur(function(){
		if($(this).val()==""){
			$(this).parents('li').addClass('error-row');
		} else {
			$(this).parents('li').removeClass('error-row');
		}
		$(this).removeClass('fc_active');
	});
	
	$(window).scroll(function(){
		if($(window).scrollTop() > $('#header').outerHeight()){
			$('.fixed').animate({
				top: $(window).scrollTop()-$('#header').outerHeight()+10
			}, {queue: false});
		} else {
			$('.fixed').animate({
				top: 0
			}, {queue: false});
		}
	});
	
	$('ol#fc_customer_billing_list li.fc_customer_company').after('<li class="clear"/>');
	$('ol#fc_customer_billing_list li.fc_customer_address2').after('<li class="clear"/>');
	$('ol#fc_customer_billing_list li.fc_customer_postal_code').after('<li class="clear"/>');
	$('ol#fc_payment_list li#fc_payment_method_plastic_container').after('<li class="clear"/>');
	
	$('a.profit-link').click(function(){
		$('.profit-select').toggle();
		return false;
	});
    $('.current-nonprofit').text($('.profit-select option:selected').text());
    $('.profit-select').change(function(){
        $('.current-nonprofit').text($('.profit-select option:selected').text());
        $('a.profit-link').click();
    })
	
	$('.tooltip').appendTo('body');
	$('.tip-load').mouseenter(function(){
		var text = $(this).attr('rel');
		var leftOff = $(this).offset().left;
		var topOff = $(this).offset().top;
		
		$('.tooltip p').html(text);
		$('.tooltip').show().css('visibility', 'hidden');
		
		var tipWidth = $('.tooltip').width();
		var tipHeight = $('.tooltip').height();
		
		$('.tooltip').css({
			'top' : topOff-tipHeight,
			'left' : leftOff-tipWidth/2 + 7,
			'visibility' : 'visible'
		});
	}).mouseleave(function(){
		$('.tooltip p').html('');
		$('.tooltip').hide();
	});

})
