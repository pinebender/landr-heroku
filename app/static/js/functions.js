$(document).ready(function() {
	// all jQuery code goes here

	//example function that executes on page load
/*	
	$(function(){
		$("#test").text("Replacement Text!");

	})
*/

	$("#showaddform").click(function()
	{
		$("#showaddform").fadeOut(0);
		$("#addform").fadeIn();
		$("#cancelbutton").fadeIn(0);
		$("#submitbutton").fadeIn(0);
		$(function() {
	  		$(document).scrollTop( $("#addform").offset().top );  
		});
		
	});

	$("#cancelbutton").click(function()
	{
		$("#addform").fadeOut(0);
		$("#submitbutton").fadeOut(0);
		$("#cancelbutton").fadeOut(0);
		$("#showaddform").fadeIn(0);
	});

	

});