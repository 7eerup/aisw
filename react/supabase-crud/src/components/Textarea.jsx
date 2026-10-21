function Textarea({ label, id, value, onChange, required = false }) {
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <textarea id={id} value={value} onChange={onChange} required={required} />
    </div>
  );
}

export default Textarea;
