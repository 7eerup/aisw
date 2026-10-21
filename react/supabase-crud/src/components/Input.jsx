function Input({ label, id, value, onChange, required = false }) {
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} value={value} onChange={onChange} required={required} />
    </div>
  );
}

export default Input;
