import '/flutter_flow/flutter_flow_animations.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'terms_of_service_model.dart';
export 'terms_of_service_model.dart';

class TermsOfServiceWidget extends StatefulWidget {
  const TermsOfServiceWidget({super.key});

  static String routeName = 'TermsOfService';
  static String routePath = 'termsOfService';

  @override
  State<TermsOfServiceWidget> createState() => _TermsOfServiceWidgetState();
}

class _TermsOfServiceWidgetState extends State<TermsOfServiceWidget>
    with TickerProviderStateMixin {
  late TermsOfServiceModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  final animationsMap = <String, AnimationInfo>{};

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => TermsOfServiceModel());

    animationsMap.addAll({
      'iconButtonOnPageLoadAnimation': AnimationInfo(
        trigger: AnimationTrigger.onPageLoad,
        effectsBuilder: () => [
          FadeEffect(
            curve: Curves.easeInOut,
            delay: 0.0.ms,
            duration: 300.0.ms,
            begin: 0.0,
            end: 1.0,
          ),
          ScaleEffect(
            curve: Curves.easeInOut,
            delay: 0.0.ms,
            duration: 300.0.ms,
            begin: Offset(0.5, 1.0),
            end: Offset(1.0, 1.0),
          ),
        ],
      ),
      'textOnPageLoadAnimation': AnimationInfo(
        trigger: AnimationTrigger.onPageLoad,
        effectsBuilder: () => [
          FadeEffect(
            curve: Curves.easeInOut,
            delay: 0.0.ms,
            duration: 600.0.ms,
            begin: 0.0,
            end: 1.0,
          ),
          MoveEffect(
            curve: Curves.easeInOut,
            delay: 0.0.ms,
            duration: 600.0.ms,
            begin: Offset(0.0, 60.0),
            end: Offset(0.0, 0.0),
          ),
        ],
      ),
    });
    setupAnimations(
      animationsMap.values.where((anim) =>
          anim.trigger == AnimationTrigger.onActionTrigger ||
          !anim.applyInitialState),
      this,
    );

    WidgetsBinding.instance.addPostFrameCallback((_) => safeSetState(() {}));
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        body: Container(
          width: double.infinity,
          height: double.infinity,
          decoration: BoxDecoration(
            color: FlutterFlowTheme.of(context).primaryBackground,
            image: DecorationImage(
              fit: BoxFit.fitWidth,
              image: CachedNetworkImageProvider(
                'https://emwntndssusfaykcvurk.supabase.co/storage/v1/object/public/SafeForYou/BG_imgs/Screenshot%202025-03-03%20192537.png',
              ),
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Padding(
                padding: EdgeInsetsDirectional.fromSTEB(16.0, 44.0, 16.0, 0.0),
                child: Row(
                  mainAxisSize: MainAxisSize.max,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    FlutterFlowIconButton(
                      borderColor: Colors.transparent,
                      borderRadius: 30.0,
                      borderWidth: 1.0,
                      buttonSize: 40.0,
                      fillColor: Color(0x33090F13),
                      icon: Icon(
                        Icons.arrow_back_rounded,
                        color: FlutterFlowTheme.of(context).primaryText,
                        size: 20.0,
                      ),
                      onPressed: () async {
                        context.pop();
                      },
                    ).animateOnPageLoad(
                        animationsMap['iconButtonOnPageLoadAnimation']!),
                  ],
                ),
              ),
              Opacity(
                opacity: 0.8,
                child: Text(
                  'SAFE FOR YOU',
                  style: FlutterFlowTheme.of(context).displaySmall.override(
                        fontFamily: 'Urbanist',
                        color: Colors.white,
                        fontSize: 32.0,
                        letterSpacing: 0.0,
                        fontWeight: FontWeight.w500,
                      ),
                ).animateOnPageLoad(animationsMap['textOnPageLoadAnimation']!),
              ),
              Container(
                width: double.infinity,
                height: 500.0,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [Color(0x00090F13), Color(0x991D2429)],
                    stops: [0.0, 0.5],
                    begin: AlignmentDirectional(0.0, -1.0),
                    end: AlignmentDirectional(0, 1.0),
                  ),
                ),
                child: ListView(
                  padding: EdgeInsets.zero,
                  shrinkWrap: true,
                  scrollDirection: Axis.vertical,
                  children: [
                    Padding(
                      padding: EdgeInsets.all(24.0),
                      child: Text(
                        'TERMS OF SERVICE\n\nLast Updated: 14-03-2025\n\nWelcome to Safe For You. These Terms of Service (\"Terms\") govern your access to and use of our mobile application (\"App\") and related services. By using our App, you agree to abide by these Terms. If you do not agree, please do not use the App.\n\n1. Acceptance of Terms\n\nBy downloading, installing, or using Safe For You, you acknowledge that you have read, understood, and agreed to these Terms. We reserve the right to modify these Terms at any time, with notice provided through the App or our website.\n\n2. Services Provided\n\nSafe For You offers the following safety and emergency response features:\n\n2.1 Predictive Threat Detection\n\nAI-Powered Voice Analysis: The App analyzes voice tone and keywords to detect signs of distress and potential threats.\n\nPhysiological Monitoring: The App may track heartbeat, stress levels, and motion patterns to assess safety risks.\n\nBehavioral Insights: The App learns your daily movement patterns and predicts potential risks based on environmental and activity data.\n\n2.2 Real-Time Emergency Response\n\nUsers can alert emergency contacts and authorities with a single tap.\n\nThe App provides live location tracking to enable quick assistance.\n\nUsers can set a built-in timer for automatic emergency activation or deactivation to prevent false alarms.\n\n2.3 Community Safety Network\n\nSafe Circle: Users may opt into a network of verified volunteers and nearby Safe For You users.\n\nIn case of an emergency, users may discreetly alert nearby users for immediate assistance.\n\nPrivacy Controls: Users have full control over location-sharing settings, and all shared data is anonymized.\n\nVerified volunteers undergo training to ensure safe and responsible responses.\n\n2.4 Integration with Wearable Technology\n\nThe App supports smartwatch integration to track physiological signals such as heartbeat and stress levels.\n\nThe App remains functional across multiple devices for accessibility.\n\n3. User Responsibilities\n\nBy using Safe For You, you agree to:\n\nProvide accurate personal and emergency contact information.\n\nUse the App responsibly and not for false alarms or misleading alerts.\n\nEnsure that you have the necessary permissions for data collection (e.g., microphone, location, health data) from your device.\n\nRespect the privacy of other users and not misuse the Community Safety Network.\n\n4. Privacy and Data Usage\n\nYour privacy is important to us. By using the App, you agree to our Privacy Policy, which outlines:\n\nHow we collect, store, and use your personal and emergency-related data.\n\nThe security measures in place to protect user data.\n\nYour rights regarding data access, modification, and deletion.\n\nWe do not sell or share personal data with third parties without user consent, except as required by law or in case of emergencies.\n\n5. Limitations of Liability\n\nSafe For You is designed to enhance personal safety, but:\n\nWe do not guarantee that emergency services or contacts will respond immediately to alerts.\n\nThe AI-powered predictions and physiological monitoring may not always be accurate.\n\nThe Safe Circle feature is community-driven, and responses depend on user participation.\n\nWe are not responsible for any damages, injuries, or losses incurred due to reliance on the App.\n\n6. Account Termination\n\nWe reserve the right to suspend or terminate user accounts if:\n\nThe App is misused, including generating false emergency alerts.\n\nUsers violate any terms outlined in this agreement.\n\nThere is any unauthorized attempt to modify or misuse App features.\n\n',
                        style: FlutterFlowTheme.of(context).titleSmall.override(
                              fontFamily: 'Readex Pro',
                              color: Colors.white,
                              letterSpacing: 0.0,
                            ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
