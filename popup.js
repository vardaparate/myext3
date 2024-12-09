document.getElementById('check-price').addEventListener('click', async () => {
    const productName = document.getElementById('product-name').value.trim();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Fetching prices...';
  
    try {
      const response = await fetch('http://127.0.0.1:8000/fetch-prices', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_name: productName })
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch prices');
      }
  
      const data = await response.json();
      // resultsDiv.innerHTML = `
      //   <p><strong>Amazon:</strong> ${data.amazon || 'Not found'}</p>
      //   <p><strong>Flipkart:</strong> ${data.flipkart || 'Not found'}</p>
      //   <p><strong>Myntra:</strong> ${data.myntra || 'Not found'}</p>
      // `;

      resultsDiv.innerHTML = `
    <h3>Amazon:</h3>
    ${data.amazon && data.amazon.length > 0 ? data.amazon.map(product => `<p>${product.title}: ${product.price}</p>`).join('') : '<p>Not found</p>'}
    
    <h3>Flipkart:</h3>
    ${data.flipkart && data.flipkart.length > 0 ? data.flipkart.map(product => `<p>${product.title}: ${product.price}</p>`).join('') : '<p>Not found</p>'}

    <h3>Myntra:</h3>
    ${data.myntra && data.myntra.length > 0 ? data.myntra.map(product => `<p>${product.title}: ${product.price}</p>`).join('') : '<p>Not found</p>'}
`;



    } catch (error) {
      resultsDiv.innerHTML = `Error: ${error.message}`;
    }
  });
  