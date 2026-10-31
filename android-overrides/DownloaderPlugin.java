package com.freemusic.app;

import android.app.DownloadManager;
import android.content.Context;
import android.net.Uri;
import android.os.Environment;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/** Скачивание файла через системный DownloadManager в папку Музыка/FreeMusic. */
@CapacitorPlugin(name = "Downloader")
public class DownloaderPlugin extends Plugin {

    @PluginMethod
    public void download(PluginCall call) {
        String url = call.getString("url");
        String fileName = call.getString("fileName");
        if (url == null || fileName == null) {
            call.reject("Не указан адрес или имя файла");
            return;
        }
        Uri uri = Uri.parse(url);
        String host = uri.getHost();
        boolean allowed = "https".equals(uri.getScheme()) && host != null
                && (host.equals("archive.org") || host.endsWith(".archive.org"));
        if (!allowed) {
            call.reject("Разрешены только загрузки с archive.org");
            return;
        }
        try {
            String safe = fileName.replaceAll("[\\\\/:*?\"<>|]", "_");
            DownloadManager.Request req = new DownloadManager.Request(uri);
            req.setTitle(safe);
            req.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            req.setDestinationInExternalPublicDir(Environment.DIRECTORY_MUSIC, "FreeMusic/" + safe);
            DownloadManager dm = (DownloadManager) getContext().getSystemService(Context.DOWNLOAD_SERVICE);
            dm.enqueue(req);
            call.resolve();
        } catch (Exception e) {
            call.reject("Ошибка загрузки: " + e.getMessage());
        }
    }
}
