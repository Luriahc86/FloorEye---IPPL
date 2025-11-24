export async function uploadImage(file: File) {
  const form = new FormData();
  form.append("image", file);

  await fetch("http://localhost:5000/upload", {
    method: "POST",
    body: form,
  });
}
