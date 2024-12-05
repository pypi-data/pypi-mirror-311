# def test_init_successful_connection() -> None:
#     engine_mock = MagicMock()

#     session_mock = MagicMock()
#     exec_mock = MagicMock(return_value=True)
#     session_mock.configure_mock(**{"exec.return_value": exec_mock})

#     with (
#         patch("sqlmodel.Session", return_value=session_mock),
#         patch.object(logger, "info"),
#         patch.object(logger, "error"),
#         patch.object(logger, "warn"),
#     ):
#         try:
#             init(engine_mock)
#             connection_successful = True
#         except Exception:
#             connection_successful = False

#         assert (
#             connection_successful
#         ), "The database connection should be successful and not raise an exception."

#         # assert session_mock.exec.called_once_with(
#         #     select(1)
#         # ), "The session should execute a select statement once."

#         assert session_mock.exec.assert_called_once_with(
#             select(1)
#         ), "The session should execute a select statement once."
