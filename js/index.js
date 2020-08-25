document.addEventListener('DOMContentLoaded', () => {

  var heading = document.getElementById("change");

  heading.addEventListener('mouseover', function(event){
    event.target.style.color='white';
  });
  heading.addEventListener('mouseout', function(event){
    event.target.style.color='black';
  });

})