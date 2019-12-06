
$(document).ready(function(){

	$(window).on("resize", function(){
		$("div#categories").height($(window).height());
		mini_side = true		
		if (mini_side) {
			$("a[data-widget='pushmenu']").click()
		}
	});
	$(window).resize()
		

	$("div.card.category .card-header").on("click", function(){
		$(this).closest(".card").toggleClass("collapsed-card");
		$(this).find(".card-tools").find("i.fas").toggleClass("fa-plus").toggleClass("fa-minus");
		

	});

	new SimpleBar(document.getElementById("categories") );	
});
