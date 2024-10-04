from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment

def create_assessment(
    project_id: str, recaptcha_key: str, token: str, recaptcha_action: str
) -> Assessment:
    """创建评估以分析界面操作的风险。
    Args:
        project_id: 您的 Google Cloud 项目 ID。
        recaptcha_key: 与网站/应用关联的 reCAPTCHA 密钥
        token: 从客户端获取的已生成令牌。
        recaptcha_action: 与令牌对应的操作名称。
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # 设置要跟踪的事件的属性。
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # 构建评估请求。
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    # 检查令牌是否有效。
    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return

    # 检查是否执行了预期操作。
    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return
    else:
        # 获取风险得分和原因。
        # 如需详细了解如何解读评估，请参阅：
        # https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            print(reason)
        print(
            "The reCAPTCHA score for this token is: "
            + str(response.risk_analysis.score)
        )
        # 获取评估名称 (id)。使用此名称为评估添加注释。
        assessment_name = client.parse_assessment_path(response.name).get("assessment")
        print(f"Assessment name: {assessment_name}")
    return response
