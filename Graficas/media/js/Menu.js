$(document).ready(function(){
	$(".segundo_nivel").hide();
	$(".primer_nivel").css("cursor","pointer");
	$(".primer_nivel").click(menu);
	});

function menu()
{
	$(this).find("li.segundo_nivel").toggle("slow");	
}