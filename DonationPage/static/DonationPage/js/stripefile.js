
var stripe = Stripe('pk_test_51U1Rl1E0QWyveMIyZeQRryyHurOQSFt4hehWawaWCLc40ptfhzhPtL1o6KvcGXLS1psMhc2N9h7t9hhYuthHfCoB00TG9dM1eo');
  const appearance = {
  theme: 'flat', // 'stripe', 'night', 'flat', or 'none'
  variables: {
    spacingUnit: '4px',     // Controls internal layout spacing
    borderRadius: '8px',    // Controls card corners
  },
  rules: {
    '.Input': {
      padding: '12px',      // This is how you change internal input height safely!
    }
  }
};

    var elements = stripe.elements({clientSecret: STRIPE_CLIENT_SECRET, appearance:appearance});    
    var paymentElement = elements.create('payment',  );
    paymentElement.mount('#payment-element');
    
    // this is the code that stops the page from reloading keeping the user and waiting for stripe
  const form = document.getElementById('payment-form')
  form.addEventListener('submit', function(event) {
  event.preventDefault();
  
  const button = document.querySelector('button[type="submit"]');
  const buttonText = 'pay';
  
  button.disabled = true;
  button.textContent = 'processing';

  stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: return_url,
    }, redirect: 'if_required'
  })
  .then(function(result) {
    if (result.error) {
      console.log(result.error.message);
      button.disabled = false;
      button.textContent = buttonText;
    }
    
    // Fixed string 'succeeded' and proper redirect assignment
    if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
      button.textContent = 'successful';
      window.location.href = return_url;
    }
  });
});
