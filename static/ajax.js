// const retrieve_count = (review_ID) => {
// 	$.getJSON('get_useful_count', review_ID, (data) => {
//         $("#useful1").text(data.result);
//     });
// };

$("#button1").bind("click", (review_ID) => {
	$.getJSON($SCRIPT_ROOT + '/get_useful_count/', review_ID, (data) => {
        $("#useful1").text(data.result);
    });
});