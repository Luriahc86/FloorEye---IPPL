export function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, _) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.readAsDataURL(file);
  });
}
