import '/flutter_flow/flutter_flow_util.dart';
import 'add_contact_widget.dart' show AddContactWidget;
import 'package:flutter/material.dart';

class AddContactModel extends FlutterFlowModel<AddContactWidget> {
  ///  State fields for stateful widgets in this component.

  // State field(s) for NameAdd widget.
  FocusNode? nameAddFocusNode;
  TextEditingController? nameAddTextController;
  String? Function(BuildContext, String?)? nameAddTextControllerValidator;
  // State field(s) for NumberAdd widget.
  FocusNode? numberAddFocusNode;
  TextEditingController? numberAddTextController;
  String? Function(BuildContext, String?)? numberAddTextControllerValidator;

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    nameAddFocusNode?.dispose();
    nameAddTextController?.dispose();

    numberAddFocusNode?.dispose();
    numberAddTextController?.dispose();
  }
}
