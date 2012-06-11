$(document).ready(function(){
	$(".createaccount").click(function(){
		$("#login_container").toggle();
		$("#register_container").toggle();
	});
	$("#submit_login").click(function(evt) {
		evt.preventDefault();
		$(".username_group").removeClass("error");
		$(".password_group").removeClass("error");
		$(".username_helper").addClass('hide');
		$(".password_helper").addClass('hide');
		$.post('/profile/login/', {
			username: $("#username").val(),
			password: $("#password").val(),
			remember_me: ($("#remember_me").attr("checked") !== undefined ? 'true' : 'false')
		}, function(data) {
			if (data) {
				if(data.success){
					window.location.reload();
				}else{
					if(data.error === "username"){
						$(".username_group").addClass("error");
						$(".username_helper").removeClass('hide');
					}
					else{
						$(".password_group").addClass("error");
						$(".password_helper").removeClass('hide');
					}
				}
			}
			else{
				console.log("server_error");
			}
		});
	});
	$("#submit_register").click(function(evt) {
		evt.preventDefault();
		$('.register_username_group').removeClass('error');
		$('.register_email_group').removeClass('error');
		$('.register_password_helper').addClass('hide');
		$(".register_email_helper_notemail").addClass('hide');
		$(".register_email_helper").addClass('hide');
		$('.register_password_group').removeClass('error');
		if ($("#register_username").val() === ""){
			$('.register_username_group').addClass('error');
		}
		else if ($("#register_email").val() === ""){
			$('.register_email_group').addClass('error');
		}
		else if ($("#register_password").val().length < 4 || $("#register_password").val().length > 30){
			$('.register_password_helper').removeClass('hide');
			$('.register_password_group').addClass('error');
		}
		else{
			$.post('/profile/create/', {
				username: $("#register_username").val(),
				email: $("#register_email").val(),
				password: $("#register_password").val(),
				remember_me: ($("#remember_me_register").attr("checked") !== undefined ? 'true' : 'false')
			}, function(data) {
				if (data) {
					if(data.success){
						window.location.reload();
					}else{
						for (var i in data.errors){
							if( data.errors[i] == 'notemail'){
								$(".register_email_group").addClass("error");
								$(".register_email_helper_notemail").removeClass('hide');
							}
							if( data.errors[i] == 'emailexists'){
								$(".register_email_group").addClass("error");
								$(".register_email_helper").removeClass('hide');
							}
							if( data.errors[i] == 'usernameexists'){
								$(".register_username_group").addClass("error");
								$(".register_username_helper").removeClass('hide');
							}
							if( data.errors[i] == 'passwordlength'){
								$(".register_password_group").addClass("error");
								$(".register_password_helper").removeClass('hide');
							}
						}
					}
				}
				else{
					console.log("server_error");
				}
			});	
		}
	});
	$(".logout").click(function(evt) {
		evt.preventDefault();
		$.get('/accounts/logout', {},
			function(data) {
				console.log(data);
				if (data && data.success) {
					window.location.reload();
				}
			}
		);
	});
	$('.login_button').click(function(evt){
		$("#loginModal").modal({backdrop:false});
	});
});

$(function() {
		
});