$(document).ready(function(){
    
    $('.intake_item').animate({
        opacity: 1
    });

    $('#intake_add').click(function(){
        pywebview.api.test('arg');
    });
  
  });