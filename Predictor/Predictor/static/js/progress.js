function setProgressBar() {
    document.getElementById('container').innerHTML="<div class=\"row\"><div id=\"alertbar\"> </div></div>"
    document.getElementById('alertbar').innerHTML="<div class=\"alert alert-warning\"> <strong>Loading!</strong> Importing large projects may take up to 15 minutes! <div class=\"progress\"> <div class=\"progress-bar progress-bar-striped active\" role=\"progressbar\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width:100%\"></div></div></div>"
    document.getElementById('subbutton').visibility = 'hidden'
}
