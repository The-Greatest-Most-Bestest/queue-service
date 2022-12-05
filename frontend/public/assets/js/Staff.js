/* eslint-disable no-undef */
// Global value to contain list of queue IDs
var categoriesList;
function getCategoryID() {
	// send HTTP request to get the categories IDs
	$.ajax({
		url: 'http://cpp-queue.com/categories?space=games-room',

		success: function (result) {
			console.log('categories success!');
			console.log(result.categories);

			// store the results to categoriesList
			categoriesList = result.categories;

			// create/update category drop down menu for the waitlist form and status
			$('#category_id_cancel').empty();
			$('#category_id_check').empty();
			for (let i = 0; i < categoriesList.length; i++) {
				let item_id = categoriesList[i].id;
				let item_name = categoriesList[i].name;

				let category_item_list =
					"<option value='" + item_id + "'>" + item_name + '</option>';
				$('#category_id_cancel').append(category_item_list);
				$('#category_id_check').append(category_item_list);
			}
		},
	});
}

function checkin() {
    console.log('notify button clicked');

    // get input from notify form
    var category_id = $('#category_id_check').val();

    console.log('Attempt to notify first person in category: ' +category_id);

    // HTTP request to notify first person in waitlist
    $.ajax({
        url:
            'http://cpp-queue.com/check-in?id=' +category_id,
        success: function(result) {
            console.log('Success!');
            alert(result);
        },
        error: function(result) {
            console.log('Error!');
            alert(result);
        },
    });
}

function cancel() {
    console.log('cancel button clicked');

    // get input from cancel form
    var category_id = $('#category_id_cancel').val();
    var uid = $('#uid').val();

    console.log('Attempt to cancel ' +uid+ ' from category: ' +category_id);

    // HTTP request to remove uid from category
    $.ajax({
        url:
            'http://cpp-queue.com/cancel?' + 
            'cid=' +category_id +
            '&uid=' +uid,
        success: function(result) {
            console.log('Success!');
            alert(result);
        },
        error: function(result) {
            console.log('Error!');
            alert(result);
        },
    });

    // Clear form
    document.getElementById('#uid').value = '';
}
