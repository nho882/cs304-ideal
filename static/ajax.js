
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
			// Once a user upvotes, the button should be disabled.
			$(el).prop("disabled",true);

		});
	});
};

$(document).ready(start);
