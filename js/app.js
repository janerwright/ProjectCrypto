document.addEventListener('DOMContentLoaded', function(event){
    var dataText=["Cyber Awareness"]
    function typeWriter(text,i, fnCallback){
        if(i<(text.length)){
            document.querySelector("h1").innerhtml=text.substring(0, i+1)
            +'<span aria-hidden="true"></span>';
        }
    }
}