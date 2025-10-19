import 'package:sqflite/sqflite.dart';

// Database Helper for Offline Storage
class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('plant_disease.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = '$dbPath/$filePath';

    return await openDatabase(path, version: 1, onCreate: _createDB);
  }

  Future _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE predictions (
        id TEXT PRIMARY KEY,
        timestamp TEXT,
        predicted_class TEXT,
        confidence REAL,
        image_path TEXT,
        severity TEXT,
        synced INTEGER DEFAULT 0,
        metadata TEXT
      )
    ''');

    await db.execute('''
      CREATE TABLE feedback (
        id TEXT PRIMARY KEY,
        prediction_id TEXT,
        correct_class TEXT,
        comments TEXT,
        timestamp TEXT,
        synced INTEGER DEFAULT 0
      )
    ''');
  }

  Future<void> insertPrediction(Map<String, dynamic> prediction) async {
    final db = await database;
    await db.insert('predictions', prediction,
        conflictAlgorithm: ConflictAlgorithm.replace);
  }

  Future<List<Map<String, dynamic>>> getUnsyncedPredictions() async {
    final db = await database;
    return await db.query('predictions', where: 'synced = ?', whereArgs: [0]);
  }

  Future<void> markAsSynced(String id) async {
    final db = await database;
    await db.update('predictions', {'synced': 1},
        where: 'id = ?', whereArgs: [id]);
  }

  Future<List<Map<String, dynamic>>> getAllPredictions({int limit = 50}) async {
    final db = await database;
    return await db.query('predictions',
        orderBy: 'timestamp DESC', limit: limit);
  }

  Future<void> insertFeedback(Map<String, dynamic> feedback) async {
    final db = await database;
    await db.insert('feedback', feedback,
        conflictAlgorithm: ConflictAlgorithm.replace);
  }
}