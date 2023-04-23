
    // instance of the Stripe object creation (from API)
    const data = document.currentScript.dataset;
    const book_id = data.book_id;
    console.log(data);
    fetch("/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
    // Stripe.js initialization
    const stripe = Stripe(data.publicKey);

    let checkoutButton = document.getElementById('checkout-button');

    checkoutButton.addEventListener('click', function () {

        let email = document.getElementById('email').value;
        if (email.length == 0) {
            alert("Please enter your email address.");
            return;
        }

        // Checkout Session via server-side endpoint
        fetch("/create-checkout-session/" + book_id +"/", {
            method: 'POST',
            body: JSON.stringify(
                { email: email }
            )
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (session) {
                return stripe.redirectToCheckout({ sessionId: session.sessionId });
            })
            .then(function (result) {
                if (result.error) {
                    alert(result.error.message);
                }
            })
            .catch(function (error) {
                console.error('Error:', error);
            });
    });
   });