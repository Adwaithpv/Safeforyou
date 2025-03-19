import 'dart:async';

import 'package:collection/collection.dart';

import '/backend/schema/util/firestore_util.dart';

import 'index.dart';
import '/flutter_flow/flutter_flow_util.dart';

class EmergencyContactsRecord extends FirestoreRecord {
  EmergencyContactsRecord._(
    DocumentReference reference,
    Map<String, dynamic> data,
  ) : super(reference, data) {
    _initializeFields();
  }

  // "Name" field.
  String? _name;
  String get name => _name ?? '';
  bool hasName() => _name != null;

  // "Number" field.
  double? _number;
  double get number => _number ?? 0.0;
  bool hasNumber() => _number != null;

  void _initializeFields() {
    _name = snapshotData['Name'] as String?;
    _number = castToType<double>(snapshotData['Number']);
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('Emergency_contacts');

  static Stream<EmergencyContactsRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => EmergencyContactsRecord.fromSnapshot(s));

  static Future<EmergencyContactsRecord> getDocumentOnce(
          DocumentReference ref) =>
      ref.get().then((s) => EmergencyContactsRecord.fromSnapshot(s));

  static EmergencyContactsRecord fromSnapshot(DocumentSnapshot snapshot) =>
      EmergencyContactsRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static EmergencyContactsRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      EmergencyContactsRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'EmergencyContactsRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is EmergencyContactsRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createEmergencyContactsRecordData({
  String? name,
  double? number,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'Name': name,
      'Number': number,
    }.withoutNulls,
  );

  return firestoreData;
}

class EmergencyContactsRecordDocumentEquality
    implements Equality<EmergencyContactsRecord> {
  const EmergencyContactsRecordDocumentEquality();

  @override
  bool equals(EmergencyContactsRecord? e1, EmergencyContactsRecord? e2) {
    return e1?.name == e2?.name && e1?.number == e2?.number;
  }

  @override
  int hash(EmergencyContactsRecord? e) =>
      const ListEquality().hash([e?.name, e?.number]);

  @override
  bool isValidKey(Object? o) => o is EmergencyContactsRecord;
}
