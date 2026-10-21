function ErrorState({ message = '요청에 실패했습니다.' }) {
  return <p role="alert">{message}</p>;
}

export default ErrorState;
