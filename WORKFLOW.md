# AI Agents - Tanımlar ve Çalışma Sırası

## Tüm Agentlar

### Geliştirme (Development)
- **CodeGenerationAgent** - Kod üretir
- **CodeReviewAgent** - Kod incelemesi yapar
- **TestGenerationAgent** - Testler oluşturur

### Analiz (Analysis)
- **ArchitectureAdvisorAgent** - Mimari tavsiyesi verir
- **TechnologySelectionAgent** - Teknoloji seçimi yapar
- **CodeAnalysisAgent** - Kod analizi yapar

### Bakım (Maintenance)
- **DebuggingAgent** - Hata ayıklama yapar
- **RefactoringAgent** - Kod refaktörü yapar
- **DocumentationAgent** - Dokümantasyon oluşturur

### İş Akışı (Workflow)
- **ProjectPlanningAgent** - Proje planlaması yapar
- **TaskManagementAgent** - Görev yönetimi yapar
- **CICDAgent** - CI/CD konfigürasyonu yapar

### Güvenlik (Security)
- **SecurityAgent** - Güvenlik açıklarını tespit eder

### Kalite (Quality)
- **PerformanceAgent** - Performans optimizasyonu yapar
- **ComplianceAgent** - Standartlara uygunluk kontrolü yapar

### Veri (Data)
- **DatabaseAgent** - Veritabanı şeması tasarlar
- **APIAgent** - API tasarımı ve dokümantasyonu yapar
- **IntegrationAgent** - Entegrasyonları yönetir

### Operasyon (Operations)
- **MonitoringAgent** - Monitoring ve logging kurulumu yapar
- **ScalingAgent** - Ölçeklendirme stratejileri belirler
- **MigrationAgent** - Veri ve kod migrasyonu yönetir

### UI/UX
- **UIUXAgent** - Arayüz önerileri sağlar

---

## Agent Çalışma Sırası

### Faz 1: Planlama (Phase 1)
1. **ProjectPlanningAgent** - Proje yapısını ve kilometre taşlarını belirle
2. **TechnologySelectionAgent** - Uygun teknoloji yığını seç
3. **ArchitectureAdvisorAgent** - Mimari kararları al
4. **DatabaseAgent** - Veritabanı şemasını tasarla
5. **APIAgent** - API yapısını belirle
6. **UIUXAgent** - Arayüz önerileri al

### Faz 2: Geliştirme (Phase 2)
7. **CodeGenerationAgent** - İlk kodu üret
8. **IntegrationAgent** - Entegrasyonları planla
9. **TestGenerationAgent** - Testler oluştur
10. **CodeReviewAgent** - Kodu incele

### Faz 3: Kalite ve Güvenlik (Phase 3)
11. **SecurityAgent** - Güvenlik açıklarını tespit et
12. **PerformanceAgent** - Performans analizı yap
13. **ComplianceAgent** - Standartlara uygunluk kontrolü

### Faz 4: İyileştirme (Phase 4 - Döngüsel)
14. **DebuggingAgent** - Hataları tespit et (gerekirse)
15. **RefactoringAgent** - Kodu iyileştir (gerekirse)

### Faz 5: Operasyon (Phase 5)
16. **MonitoringAgent** - Monitoring sistemi kur
17. **ScalingAgent** - Ölçeklendirme stratejisi belirle
18. **MigrationAgent** - Migrasyon planı hazırla (gerekirse)

### Faz 6: Dokümantasyon (Phase 6)
19. **DocumentationAgent** - Dokümantasyon oluştur

### Faz 7: Dağıtım (Phase 7)
20. **CICDAgent** - CI/CD pipeline konfigüre et
21. **TaskManagementAgent** - Görevleri takip et (devam eden süreç)

---

## Notlar

### Döngüsel Fazlar
- Faz 4 (İyileştirme) gerektiğinde birden fazla kez tekrarlanabilir
- Her döngü sonunda CodeReviewAgent çalıştırılmalı

### Esnek Kullanım
- **CodeAnalysisAgent** istenildiği zaman kullanılabilir
- **TaskManagementAgent** tüm süreç boyunca aktif olabilir
- **SecurityAgent**, **PerformanceAgent**, **ComplianceAgent** geliştirme sürecinin her aşamasında çalıştırılabilir

### Minimum Sıralama
Küçük projeler için minimum sıralama:
1. ProjectPlanningAgent → 2. TechnologySelectionAgent → 3. ArchitectureAdvisorAgent → 4. CodeGenerationAgent → 5. TestGenerationAgent → 6. CICDAgent