<script type="text/javascript" src="../media/js/jquery-1.8.2.js"></script>
$(document).ready(iniciar)
function iniciar()
{		
	$("table#1").hide();
	$("table#1 tr:first").css("font-weight","bold");
	$("div#0").css("cursor","pointer");
	$("table#1 tr:last").css("font-weight","bold");
	$("table#1 tr:even").css("background-color","#CEEFFF");
	$("div#0").click(function()
	{	if($("table#1").is (':hidden')){
		$("table#1").show();
		$("div#0 h1").text("Presiona para ocultar la tabla");}
		else{
		$("table#1").hide();
		$("div#0 h1").text("Presiona para ver la tabla");
		}
	});	
	
}