# AI Agents Projesi

Bu proje, yazılım geliştirme süreçlerinde kullanılmak üzere tasarlanmış AI agentlar koleksiyonudur.

## Yapı

```
agents/
├── development/          # Geliştirme agentları
│   ├── code_generation_agent.py
│   ├── code_review_agent.py
│   └── test_generation_agent.py
├── analysis/            # Analiz agentları
│   ├── architecture_advisor_agent.py
│   ├── technology_selection_agent.py
│   └── code_analysis_agent.py
├── maintenance/         # Bakım agentları
│   ├── debugging_agent.py
│   ├── refactoring_agent.py
│   └── documentation_agent.py
├── workflow/            # İş akışı agentları
│   ├── project_planning_agent.py
│   ├── task_management_agent.py
│   └── cicd_agent.py
├── security/            # Güvenlik agentları
│   └── security_agent.py
├── quality/             # Kalite agentları
│   ├── performance_agent.py
│   └── compliance_agent.py
├── data/                # Veri agentları
│   ├── database_agent.py
│   ├── api_agent.py
│   └── integration_agent.py
├── operations/          # Operasyon agentları
│   ├── monitoring_agent.py
│   ├── scaling_agent.py
│   └── migration_agent.py
└── uiux/                # UI/UX agentları
    └── uiux_agent.py
```

## Kullanım

Her agent `BaseAgent` sınıfından kalıtım alır ve `execute` metodunu uygular.

## Agent Listesi

### Geliştirme (Development)
- CodeGenerationAgent: Kod üretir
- CodeReviewAgent: Kod incelemesi yapar
- TestGenerationAgent: Testler oluşturur

### Analiz (Analysis)
- ArchitectureAdvisorAgent: Mimari tavsiyesi verir
- TechnologySelectionAgent: Teknoloji seçimi yapar
- CodeAnalysisAgent: Kod analizi yapar

### Bakım (Maintenance)
- DebuggingAgent: Hata ayıklama yapar
- RefactoringAgent: Kod refaktörü yapar
- DocumentationAgent: Dokümantasyon oluşturur

### İş Akışı (Workflow)
- ProjectPlanningAgent: Proje planlaması yapar
- TaskManagementAgent: Görev yönetimi yapar
- CICDAgent: CI/CD konfigürasyonu yapar

### Güvenlik (Security)
- SecurityAgent: Güvenlik açıklarını tespit eder

### Kalite (Quality)
- PerformanceAgent: Performans optimizasyonu yapar
- ComplianceAgent: Standartlara uygunluk kontrolü yapar

### Veri (Data)
- DatabaseAgent: Veritabanı şeması tasarlar
- APIAgent: API tasarımı ve dokümantasyonu yapar
- IntegrationAgent: Entegrasyonları yönetir

### Operasyon (Operations)
- MonitoringAgent: Monitoring ve logging kurulumu yapar
- ScalingAgent: Ölçeklendirme stratejileri belirler
- MigrationAgent: Veri ve kod migrasyonu yönetir

### UI/UX
- UIUXAgent: Arayüz önerileri sağlar

## Çalışma Sırası

Detaylı çalışma sırası için [WORKFLOW.md](WORKFLOW.md) dosyasına bakın.

## Toplam Agent Sayısı: 21