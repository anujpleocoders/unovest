$( document ).ready(function() {
    $('.dropdown-item').on('click',function (){
      if($(this).attr('href')){
        alert('redirect to '+$(this).attr('href'));
        window.location.replace($(this).attr('href'));
        
         }
      
    });
  });


//     document.getElementById("output").innerHTML = location.search;
// $(".chosen-select").chosen();


function changeBedroomBtn(v1){
  $('.bedroom-btn-group .btn').removeClass('active');
  $('.bedroom-btn'+v1).addClass('active');
  // alert('.bedroom-btn'+v1)
}
function changeSchoolBtn(v1){
  $('.school-btn-group .btn').removeClass('active');
  $('.button-school'+v1).addClass('active');
  //  alert('.button-school'+v1)
}
function changeFamilyBtn(v1){
  $('.family-btn-group .btn').removeClass('active');
  $('.button-family'+v1).addClass('active');
  //  alert('.button-school'+v1)
}

function changePropertyBtn(v1){
  $('.property-btn-group .btn').removeClass('active');
  $('.button-property'+v1).addClass('active');
  //  alert('.button-school'+v1)
}

function locationClick(){
  alert('hii')
  document.getElementById("inputLocation").focus();
  $('#inputLocation').focus()
}