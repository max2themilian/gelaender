function renderProducts(products) {
  const grid = document.getElementById("shop-grid");
  if (!grid) return;

  if (!products.length) {
    grid.innerHTML = '<article class="card"><h2>Shop under construction</h2><p>First release items are being finalized.</p></article>';
    return;
  }

  grid.innerHTML = products
    .map(
      (product) => `
      <article class="card">
        <h2>${product.name}</h2>
        <p>${product.description ?? "No description yet."}</p>
        <strong>EUR ${(product.price_cents / 100).toFixed(2)}</strong>
      </article>
    `
    )
    .join("");
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const products = await window.GelaenderApi.getProducts();
    renderProducts(products);
  } catch (error) {
    renderProducts([]);
    console.error(error);
  }
});
