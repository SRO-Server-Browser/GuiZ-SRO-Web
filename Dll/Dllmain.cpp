#include <windows.h>
#include <string>

// Global değişken
static HANDLE g_hGuiZProcess = NULL; // guiZ.exe’nin süreç handle’ı

// DLL’nin yolunu bulan yardımcı fonksiyon
std::wstring GetDLLPath() {
    wchar_t path[MAX_PATH];
    HMODULE hModule = NULL;
    GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS, (LPCWSTR)GetDLLPath, &hModule);
    GetModuleFileNameW(hModule, path, MAX_PATH);
    return std::wstring(path);
}

// Export fonksiyonu (StudPE için)
extern "C" __declspec(dllexport) void StartGuiZ() {
    // DLL’nin bulunduğu klasörü al
    std::wstring dllPath = GetDLLPath();
    std::wstring::size_type pos = dllPath.find_last_of(L"\\");
    std::wstring dllDir = dllPath.substr(0, pos); // DLL’nin klasörü
    std::wstring exePath = dllDir + L"\\guiZ.exe"; // guiZ.exe aynı dizinde

    // Log: guiZ.exe yolu
    std::wstring logMsg = L"guiZ.exe yolu: " + exePath + L"\n";
    OutputDebugString(logMsg.c_str());

    // guiZ.exe’yi çalıştır
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };
    BOOL success = CreateProcess(
        exePath.c_str(),   // guiZ.exe yolu
        NULL,              // Komut satırı parametreleri
        NULL,              // Süreç handle miras alınmasın
        NULL,              // Thread handle miras alınmasın
        FALSE,             // Handle miras alma kapalı
        CREATE_NO_WINDOW,  // Penceresiz çalışsın
        NULL,              // Ortam değişkenleri
        NULL,              // Çalışma dizini
        &si,               // Startup info
        &pi                // Süreç bilgisi
    );

    if (success) {
        // Süreç handle’ını global değişkene kaydet
        g_hGuiZProcess = pi.hProcess;
        CloseHandle(pi.hThread);
        OutputDebugString(L"guiZ.exe başarıyla başlatıldı!\n");
    }
    else {
        // Hata mesajı
        DWORD error = GetLastError();
        wchar_t errorMsg[256];
        FormatMessageW(FORMAT_MESSAGE_FROM_SYSTEM, NULL, error, 0, errorMsg, 256, NULL);
        std::wstring errorLog = L"guiZ.exe başlatılamadı! Hata: " + std::wstring(errorMsg) + L"\n";
        OutputDebugString(errorLog.c_str());
    }
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH: {
        StartGuiZ(); // guiZ.exe’yi başlat
        break;
    }
    case DLL_PROCESS_DETACH: {
        // guiZ.exe’yi sonlandır
        if (g_hGuiZProcess != NULL) {
            TerminateProcess(g_hGuiZProcess, 0);
            CloseHandle(g_hGuiZProcess);
            g_hGuiZProcess = NULL;
            OutputDebugString(L"guiZ.exe sonlandırıldı!\n");
        }
        break;
    }
    }
    return TRUE;
}
