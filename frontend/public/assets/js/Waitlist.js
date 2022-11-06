/* eslint-disable no-undef */
function waitlist() {
	console.log('clicked!');

	// get the input
	var category = $('#category_id').val();
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
	console.log('Item id: ' + category);
	console.log('Name: ' + name);
	console.log('UID: ' + uid);
	console.log('Email: ' + email);
	console.log('Phone: ' + phone);

	//send the HTTP request
	$.ajax({
		url:
			'http://cpp-queue.com/add?id=' +
			category +
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

			var billiard_id = '2cda2c0a-e0f0-4a62-9352-3bfbe76ece41';
			var ns_id = '147bda7c-ff1d-424a-abb9-0b76ea714d74';
			var ps4_id = '7a08baeb-7380-4d76-a50f-f874543b397b';
			var xbox_id = '5be0be93-933f-4f11-8622-f6b3795a1c48';
			var pingpong_id = '48d840c9-0485-4694-bc0c-68216d33acf7';
			var item = '';

			switch (category) {
				case ns_id:
					item = 'Nintendo Switch';
					break;
				case ps4_id:
					item = 'PS4';
					break;
				case xbox_id:
					item = 'Xbox';
					break;
				case pingpong_id:
					item = 'Ping Pong';
					break;
				default:
					item = 'Billiard';
			}

			alert(
				'CONGRATULATIONS! \nYour waitlist position for ' +
					item +
					' is ' +
					result.position +
					'. \nYou can also check under Waitlist Status to see your position in the waitlist.'
			);

			// render the result in the page
			var waitlists = result;
			// Billiard
			if (category === billiard_id) {
				// update the waitlist table
				let v =
					'<tr> <td>Billiard</td> <td>' +
					name +
					'</td> <td>' +
					waitlists.position +
					'</td> </tr>';
				$('#waitlist_table').append(v);
				// update the total number of people in billiard waitlist
				let bill =
					"<span class='badge badge-primary badge-pill'>" +
					waitlists.position +
					'</span>';
				$('#bill_position').html(bill);
			}
			// Nintendo Swtich
			else if (category === ns_id) {
				// update the waitlist table
				let v =
					'<tr> <td>Nintendo Switch</td> <td>' +
					name +
					'</td> <td>' +
					waitlists.position +
					'</td> </tr>';
				$('#waitlist_table').append(v);
				// update the total number of people in nintendo switch waitlist
				let ns =
					"<span class='badge badge-primary badge-pill'>" +
					waitlists.position +
					'</span>';
				$('#ns_position').html(ns);
			}
			// PS4
			else if (category === ps4_id) {
				// update the waitlist table
				let v =
					'<tr> <td>PS4</td> <td>' +
					name +
					'</td> <td>' +
					waitlists.position +
					'</td> </tr>';
				$('#waitlist_table').append(v);
				// update the total number of people in PS4 waitlist
				let ps4 =
					"<span class='badge badge-primary badge-pill'>" +
					waitlists.position +
					'</span>';
				$('#ps4_position').html(ps4);
			}
			// Xbox
			else if (category === xbox_id) {
				// update the waitlist table
				let v =
					'<tr> <td>Xbox</td> <td>' +
					name +
					'</td> <td>' +
					waitlists.position +
					'</td> </tr>';
				$('#waitlist_table').append(v);
				// update the total number of people in xbox waitlist
				let xbox =
					"<span class='badge badge-primary badge-pill'>" +
					waitlists.position +
					'</span>';
				$('#xbox_position').html(xbox);
			}
			// Ping Pong
			else if (category === pingpong_id) {
				// update the waitlist table
				let v =
					'<tr> <td>Ping Pong</td> <td>' +
					name +
					'</td> <td>' +
					waitlists.position +
					'</td> </tr>';
				$('#waitlist_table').append(v);
				// update the total number of people in pingpong waitlist
				let pingpong =
					"<span class='badge badge-primary badge-pill'>" +
					waitlists.position +
					'</span>';
				$('#pingpong_position').html(pingpong);
			}
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
	document.getElementById('category_id').value =
		'2cda2c0a-e0f0-4a62-9352-3bfbe76ece41';
	document.getElementById('name').value = '';
	document.getElementById('uid').value = '';
	document.getElementById('email').value = '';
	document.getElementById('phone').value = '';
}

// Sort waitlist on a button click
function sortTable() {
	var table, i, x, y;
	table = document.getElementById('waitlist_table');
	var switching = true;

	// Run loop until no switching is needed
	while (switching) {
		switching = false;
		var rows = table.rows;

		// loop to go through all rows
		for (i = 1; i < rows.length - 1; i++) {
			var isSwitch = false;

			// fetch 3 elemenst that need to be compared
			x = rows[i].getElementsByTagName('td')[0];
			y = rows[i + 1].getElementsByTagName('td')[0];

			// check if 3 rows need to be switched
			if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
				// If yes, mark isSwitch as needed and break loop
				isSwitch = true;
				break;
			}
		}
		if (isSwitch) {
			// Function to switch rows and mark switching as completed
			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
			switching = true;
		}
	}
}

// verify correct phone number format
function validatePhoneNumber(input_str) {
	// using Regex to check phone number format
	var re = /^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/;

	return re.test(input_str);
}
