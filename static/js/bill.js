
(function( $ ) {
 function getCookie(name) {
 var cookieValue = null;
 if (document.cookie && document.cookie != '') {
 var cookies = document.cookie.split(';');
 for (var i = 0; i < cookies.length; i++) {
 var cookie = jQuery.trim(cookies[i]);
 // Does this cookie string begin with the name we want?
 if (cookie.substring(0, name.length + 1) == (name + '=')) {
 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
 break;
 }
 }
 }
 return cookieValue;
 }
 
 var csrftoken = getCookie('csrftoken');
 $.ajaxSetup({
             beforeSend: function(xhr) {
             xhr.setRequestHeader("X-CSRFToken", csrftoken);
             }
             });
 })(jQuery);




// AJAX for posting

function create_post() {
    console.log("create post is working!"); // sanity check
    (function( $ ) {
     $.ajax({
            url : "create_post/", // the endpoint
            type : "POST", // http method
            data : { the_post : $('#post-text').val() }, // data sent with the post request
            
            // handle a successful response
            success : function(response) {
            $('#post-text').val(''); // remove the value from the input
            //console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if (response.status == 'added') {
            $("#favourite").removeClass('far').addClass('fa');
            console.log("add star");
            }
            else {
            $("#favourite").removeClass('fa').addClass('far');
            //$('#favourite')).removeClass('fa-star').addClass('fa-star-empty');
            console.log("remove star");
            }
            //$obj.parent('.favorite').children('.fav-count').text(response.fav_count);
            //$obj.prop('disabled', false);
            },
            
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                               " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
            });
     })(jQuery);
};





// Submit post on submit
(function( $ ) {
 $('#post-form').on('submit', function(event){
                    event.preventDefault();
                    console.log("form submitted!")  // sanity check
                    create_post();
                    });
 })(jQuery);


(function( $ ) {
 $(function() {
   $('#ridings-small').change(function(){
                        $('.tdsinfo-small').hide();
                        $('#' + $(this).val()).show();
                        });
   });
 })(jQuery);

(function( $ ) {
 $(function() {
   $('#ridings').change(function(){
                        $('.tdsinfo').hide();
                        $('#' + $(this).val()).show();
                        });
   });
 })(jQuery);



function show1(){
    document.getElementById('div0').style.display ='none';
    document.getElementById('div1').style.display ='';
    document.getElementById('div2').style.display = 'none';
    document.getElementById('div3').style.display = 'none';
}
function show2(){
    document.getElementById('div0').style.display ='none';
    document.getElementById('div2').style.display = '';
    document.getElementById('div1').style.display ='none';
    document.getElementById('div3').style.display = 'none';
}
function show3(){
    document.getElementById('div0').style.display ='none';
    document.getElementById('div3').style.display ='';
    document.getElementById('div1').style.display = 'none';
    document.getElementById('div2').style.display = 'none';
}

