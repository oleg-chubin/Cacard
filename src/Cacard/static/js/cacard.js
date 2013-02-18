$(function(){
  $('.full-description').hide();
  $('.info-description a').click(function(){
     $(this).closest('.description-container').find('.info-description').toggle();
  });
});
