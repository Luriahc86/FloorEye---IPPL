interface Props {
  onImageSelected: (file: File) => void;
}

export default function ImageUploader({ onImageSelected }: Props) {
  return (
    <div className="p-4 border rounded-lg bg-white shadow">
      <label className="block mb-2 text-sm font-medium">Pilih Gambar</label>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => e.target.files && onImageSelected(e.target.files[0])}
        className="w-full"
      />
    </div>
  );
}
