async function sendOTP() {

    const email = document.getElementById("email").value.trim();

    if (email === "") {

        alert("Please Enter Your Email");

        return;

    }

    try {

        const response = await fetch("/send-otp", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email: email

            })

        });

        const result = await response.json();

        if (response.ok) {

            alert(result.message);

        } else {

            alert(result.detail);

        }

    } catch (error) {

        alert("Server Error");

    }

}



async function verifyOTP() {

    const email = document.getElementById("email").value.trim();

    const otp = document.getElementById("otp").value.trim();

    if (email === "" || otp === "") {

        alert("Please Enter Email and OTP");

        return;

    }

    try {

        const response = await fetch("/verify-otp", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email: email,

                otp: otp

            })

        });

        const result = await response.json();

        if (response.ok) {

            alert(result.message);

            window.location.href = "/dashboard";

        }

        else {

            alert(result.detail);

        }

    }

    catch (error) {

        alert("Server Error");

    }

}