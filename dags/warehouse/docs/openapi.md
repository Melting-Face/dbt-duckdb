{% docs result_code %}
 | code     | message                                          | description                         |
 | -------- | ------------------------------------------------ | ----------------------------------- |
 | 00       | NORMAL_SERVICE                                   | 정상                                |
 | 01       | APPLICATION_ERROR                                | 어플리케이션 에러                   |
 | 02       | DB_ERROR                                         | 데이터베이스 에러                   |
 | 03       | NODATA_ERROR                                     | 데이터없음 에러                     |
 | 04       | HTTP_ERROR                                       | HTTP 에러                           |
 | 05       | SERVICETIME_OUT                                  | 서비스 연결실패 에러                |
 | 10       | INVALID_REQUEST_PARAMETER_ERROR                  | 잘못된 요청 파라메터 에러           |
 | 11       | NO_MANDATORY_REQUEST_PARAMETERS_ERROR            | 필수요청 파라메터가 없음            |
 | 12       | NO_OPENAPI_SERVICE_ERROR                         | 해당 오픈API서비스가 없거나 폐기됨  |
 | 20       | SERVICE_ACCESS_DENIED_ERROR                      | 서비스 접근거부                     |
 | 21       | TEMPORARILY_DISABLE_THE_SERVICEKEY_ERROR         | 일시적으로 사용할 수 없는 서비스 키 |
 | 22       | LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR | 서비스 요청제한횟수 초과에러        |
 | 30       | SERVICE_KEY_IS_NOT_REGISTERED_ERROR              | 등록되지 않은 서비스키              |
 | 31       | DEADLINE_HAS_EXPIRED_ERROR                       | 기한만료된 서비스키                 |
 | 32       | UNREGISTERED_IP_ERROR                            | 등록되지 않은 IP                    |
 | 33       | UNSIGNED_CALL_ERROR                              | 서명되지 않은 호출                  |
 | 99       | UNKNOWN_ERROR                                    | 기타에러                            |
{% enddocs %}
