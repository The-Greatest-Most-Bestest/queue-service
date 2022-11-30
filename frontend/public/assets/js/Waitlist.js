/* eslint-disable no-undef */
var categoriesList; // global variable
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
			$('#category_id').empty();
			$('#category_id_status').empty();
			for (let i = 0; i < categoriesList.length; i++) {
				let item_id = categoriesList[i].id;
				let item_name = categoriesList[i].name;

				let category_item_list =
					"<option value='" + item_id + "'>" + item_name + '</option>';
				$('#category_id').append(category_item_list);
				$('#category_id_status').append(category_item_list);

				// // create waitlist status list === NOT FIXED ===
				// let item_count_id = item_name.replaceAll(' ', '-') + '_count';
				// let item_count_title_id =
				// 	item_name.replaceAll(' ', '-') + '_count_title';
				// let span_syntax =
				// 	'<span ' +
				// 	item_count_id +
				// 	" class='badge badge-primary badge-pill'>0</span>";
				// let div_syntax =
				// 	'<div id=' +
				// 	item_count_title_id +
				// 	"class='list-group-item d-flex justify-content-between align-items-center'>" +
				// 	item_name +
				// 	' ' +
				// 	span_syntax +
				// 	'</div>';

				// console.log(div_syntax);
				// $('#waitlist-list').append(div_syntax);
			}
		},
	});
}

// join waitlist function
function waitlist() {
	console.log('clicked!');

	// get the input
	var category_id = $('#category_id').val();
	var name = $('#name').val();
	var uid = $('#uid').val();
	var email = $('#email').val();
	var phone = $('#phone').val();

	// check there all the blanks are filled out
	if ((name === '') | (uid === '') | (email === '') | (phone === '')) {
		alert('Please make sure to fill out all the blanks.');
		return;
	} else if (!validatePhoneNumber(phone)) {
		// validate phone number
		alert('Please enter the correct format phone number (ex: 909-869-4467).');
		return;
	}

	// console log
	console.log('Item id: ' + category_id);
	console.log('Name: ' + name);
	console.log('UID: ' + uid);
	console.log('Email: ' + email);
	console.log('Phone: ' + phone);

	//send the HTTP request to join waitlist
	$.ajax({
		url:
			'http://cpp-queue.com/add?id=' +
			category_id +
			'&name=' +
			name +
			'&uid=' +
			uid +
			'&email=' +
			email +
			'&phone=' +
			phone,
		success: function (result) {
			console.log('Success!');
			console.log(result);

			var item = '';
			// get item name
			for (let i = 0; i < categoriesList.length; i++) {
				if (category_id === categoriesList[i].id) {
					item = categoriesList[i].name;
				}
			}

			alert(
				'CONGRATULATIONS! \nYour waitlist position for ' +
					item +
					' is ' +
					result.position +
					'. \nYou can also check under Waitlist Status to see your position in the waitlist.'
			);

			// // render the result in the page
			// var waitlists = result;
			// for (let i = 0; i < categoriesList.length; i++) {
			// 	if (category_id === categoriesList[i].id) {
			// 		let item_name = categoriesList[i].name;

			// 		// update the waitlist table
			// 		let v =
			// 			'<tr> <td>' +
			// 			item_name +
			// 			'</td> <td>' +
			// 			name +
			// 			'</td> <td>' +
			// 			waitlists.position +
			// 			'</td> </tr>';
			// 		$('#waitlist_table').append(v);
			// 	}
			// }
		},
		// Failed to send HTTP request: user is already in the waitlist
		error: function (result) {
			console.log('Error!');

			alert(
				'Good news! You are already in the wailist. \nPlease check under Waitlist Status to see your position in the waitlist.'
			);
		},
	});

	// Clear form after submitting
	document.getElementById('category_id').value = category_id;
	document.getElementById('name').value = '';
	document.getElementById('uid').value = '';
	document.getElementById('email').value = '';
	document.getElementById('phone').value = '';
}

// // Sort waitlist on a button click
// function sortTable() {
// 	var table, i, x, y;
// 	table = document.getElementById('waitlist_table');
// 	var switching = true;

// 	// Run loop until no switching is needed
// 	while (switching) {
// 		switching = false;
// 		var rows = table.rows;

// 		// loop to go through all rows
// 		for (i = 1; i < rows.length - 1; i++) {
// 			var isSwitch = false;

// 			// fetch 3 elemenst that need to be compared
// 			x = rows[i].getElementsByTagName('td')[0];
// 			y = rows[i + 1].getElementsByTagName('td')[0];

// 			// check if 3 rows need to be switched
// 			if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
// 				// If yes, mark isSwitch as needed and break loop
// 				isSwitch = true;
// 				break;
// 			}
// 		}
// 		if (isSwitch) {
// 			// Function to switch rows and mark switching as completed
// 			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
// 			switching = true;
// 		}
// 	}
// }

// verify correct phone number format
function validatePhoneNumber(input_str) {
	// using Regex to check phone number format
	var re = /^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/;

	return re.test(input_str);
}

// returns the position in line
function checkPosition() {
	console.log('clicked!');

	// get the input
	var category_id = $('#category_id_status').val();
	var uid = $('#uid_status').val();

	// check there all the blanks are filled out
	if (uid === '') {
		alert('Please make sure to fill out all the blanks.');
		return;
	}

	$.ajax({
		url: 'http://cpp-queue.com/status?cid=' + category_id + '&uid=' + uid,

		// send HTTP request
		success: function (result) {
			console.log('check position success!');
			console.log(result.categories);

			// store the results
			var position = result.message;

			// get item name
			var item = '';
			for (let i = 0; i < categoriesList.length; i++) {
				if (category_id === categoriesList[i].id) {
					item = categoriesList[i].name;
				}
			}

			alert('Your waitlist position for ' + item + ' is ' + position + '.');
		},

		// Failed to send HTTP request: user is not in the waitlist or wrong BroncoID
		error: function (result) {
			console.log('Error!');

			alert(
				'Waitlist position not found. \nPlease enter a valid BroncoID number.'
			);
		},
	});

	// clear uid_status value
	document.getElementById('uid_status').value = '';
}
