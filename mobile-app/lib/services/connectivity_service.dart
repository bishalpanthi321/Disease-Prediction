import 'package:connectivity_plus/connectivity_plus.dart';

class ConnectivityService {
  static final ConnectivityService instance = ConnectivityService._init();
  bool _isOnline = true;

  ConnectivityService._init();

  bool get isOnline => _isOnline;

  Future<void> initialize() async {
    var connectivityResult = await Connectivity().checkConnectivity();
    _isOnline = connectivityResult != ConnectivityResult.none;

    // Listen to connectivity changes
    Connectivity().onConnectivityChanged.listen((ConnectivityResult result) {
      _isOnline = result != ConnectivityResult.none;
    });
  }

  Future<bool> checkConnectivity() async {
    var result = await Connectivity().checkConnectivity();
    _isOnline = result != ConnectivityResult.none;
    return _isOnline;
  }
}