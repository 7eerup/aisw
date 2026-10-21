function LoadingState({ message = '불러오는 중입니다...' }) {
  return <p role="status">{message}</p>;
}

export default LoadingState;
