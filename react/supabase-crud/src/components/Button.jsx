function Button({ children, type = 'button', disabled = false, onClick }) {
  return (
    <button type={type} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}

export default Button;
