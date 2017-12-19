
const start = () => {
	$(".btn.btn-primary.btn-sm.useful").each((index,el) => {
		let review_ID = $(el).val();
		let id = "useful" + (index+1);
		$.getJSON($SCRIPT_ROOT + '/get_useful_count/', {"review_ID": review_ID}, (data) => {
			$("#"+id).text(data['useful']);
	    });

		$(el).bind("click", () => {
			$.getJSON($SCRIPT_ROOT + '/update_useful_count/', {"review_ID": review_ID}, (data) => {
		        $("#"+id).text(data["usefulUpdate"]);
			});
			$(el).prop("disabled",true);

		});
	});

	$("#display-all-reviews").bind("click", () =>{
		$.getJSON($SCRIPT_ROOT + '/get-all-reviews/', (data) => {
			data.each((index, el) =>{
				// let reviewDiv = $("<div>", {"class"="content"});

			});
		});

	});

	$("#display-all-users").bind("click", () => {
		$.getJSON($SCRIPT_ROOT + '/get-all-users/', (data) => {
			console.log(data);
		});
	});
};

$(document).ready(start);
