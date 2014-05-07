$(document).ready(function() {
	// all jQuery code goes here

	//example function that executes on page load
/*	
	$(function(){
		$("#test").text("Replacement Text!");

	})
*/
	if ($("#reloadform").is('*'))
	{
		// $(document).scrollTop( $("#addform").offset().top);
	}

	$("#showaddform").click(function()
	{
		$("#showaddform").fadeOut(0);
		$("#addtask").fadeIn(0);
		$("#addreward").fadeIn(0);
		$("#cancelbutton").fadeIn(0);
		$("#submitbutton").fadeIn(0);
		// $(document).scrollTop( $("#addform").offset().top );		
	});

	$("#regclick").click(function()
	{
		$("#loginform").fadeOut(0);
		$("#regform").fadeIn();
	});

	$("#loginclick").click(function()
	{
		$("#regform").fadeOut(0);
		$("#loginform").fadeIn();
		
	});

});