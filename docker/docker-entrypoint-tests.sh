#!/bin/bash
# ============================================================================
# ENTRYPOINT PARA TESTES - EVAonline (Pytest)
# ============================================================================
# Este script executa todos os testes do backend com pytest + coverage
# Usado pelo serviço test-runner no docker-compose.yml

set -e  # Exit on error

echo "============================================================================"
echo "🧪 SISTEMA DE TESTES - EVAonline (Pytest Framework)"
echo "============================================================================"
echo ""
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Container ID: $(hostname)"
echo "Ambiente: ${ENVIRONMENT:-testing}"
echo "Python: $(python --version)"
echo "Pytest: $(pytest --version)"
echo ""

# ============================================================================
# AGUARDAR SERVIÇOS SEREM SAUDÁVEIS
# ============================================================================

echo "⏳ Aguardando PostgreSQL..."
max_attempts=30
attempt=0
while ! nc -z postgres 5432; do
    if [ $attempt -ge $max_attempts ]; then
        echo "❌ PostgreSQL não respondeu após $max_attempts tentativas"
        exit 1
    fi
    attempt=$((attempt + 1))
    echo "   Tentativa $attempt/$max_attempts..."
    sleep 1
done
echo "✅ PostgreSQL pronto"

echo ""
echo "⏳ Aguardando Redis..."
attempt=0
while ! redis-cli -h redis -a "${REDIS_PASSWORD}" ping > /dev/null 2>&1; do
    if [ $attempt -ge $max_attempts ]; then
        echo "❌ Redis não respondeu após $max_attempts tentativas"
        exit 1
    fi
    attempt=$((attempt + 1))
    echo "   Tentativa $attempt/$max_attempts..."
    sleep 1
done
echo "✅ Redis pronto"

echo ""

# ============================================================================
# EXECUTAR MIGRATIONS (ALEMBIC)
# ============================================================================

echo "🔄 Executando migrações do banco de dados..."
cd /app

if [ -d "alembic" ] && [ -f "alembic.ini" ]; then
    echo "   Executando: alembic upgrade heads"
    alembic upgrade heads
    echo "✅ Migrações concluídas"
else
    echo "⚠️  Alembic não encontrado, pulando migrações"
fi

echo ""

# ============================================================================
# EXECUTAR TESTES COM PYTEST
# ============================================================================

echo "============================================================================"
echo "🧪 INICIANDO TESTES COM PYTEST"
echo "============================================================================"
echo ""

# Detectar tipo de teste solicitado (via variável de ambiente)
TEST_TYPE="${TEST_TYPE:-all}"

case "$TEST_TYPE" in
    "unit")
        echo "📦 Rodando apenas TESTES UNITÁRIOS..."
        PYTEST_ARGS="backend/tests/unit/ -m unit"
        ;;
    "integration")
        echo "🔗 Rodando apenas TESTES DE INTEGRAÇÃO..."
        PYTEST_ARGS="backend/tests/integration/ -m integration"
        ;;
    "e2e")
        echo "🌐 Rodando apenas TESTES E2E..."
        PYTEST_ARGS="backend/tests/e2e/ -m e2e"
        ;;
    "performance")
        echo "⚡ Rodando apenas TESTES DE PERFORMANCE..."
        PYTEST_ARGS="backend/tests/performance/ -m performance"
        ;;
    "security")
        echo "🔒 Rodando apenas TESTES DE SEGURANÇA..."
        PYTEST_ARGS="backend/tests/security/ -m security"
        ;;
    "critical")
        echo "🔥 Rodando apenas TESTES CRÍTICOS (unit + integration)..."
        PYTEST_ARGS="backend/tests/unit/ backend/tests/integration/ -m 'unit or integration'"
        ;;
    "fast")
        echo "⚡ Rodando apenas TESTES RÁPIDOS (excluindo slow)..."
        PYTEST_ARGS="backend/tests/ -m 'not slow'"
        ;;
    *)
        echo "🎯 Rodando TODOS OS TESTES..."
        PYTEST_ARGS="backend/tests/"
        ;;
esac

# Executar pytest com coverage
pytest $PYTEST_ARGS \
    --verbose \
    --color=yes \
    --tb=short \
    --cov=backend \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-report=xml:coverage.xml \
    --junit-xml=junit.xml \
    --maxfail=5 \
    --durations=10

# Capturar código de saída
EXIT_CODE=$?

echo ""

# ============================================================================
# RESUMO FINAL
# ============================================================================

echo "============================================================================"
echo "📊 RESUMO DOS TESTES"
echo "============================================================================"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo "🎉 TODOS OS TESTES PASSARAM!"
    echo "   Backend está operacional e pronto para uso."
    echo ""
    echo "📈 Relatórios gerados:"
    echo "   - HTML: htmlcov/index.html"
    echo "   - XML: coverage.xml"
    echo "   - JUnit: junit.xml"
    exit 0
else
    echo "⚠️  ALGUNS TESTES FALHARAM (exit code: $EXIT_CODE)"
    echo "   Verifique os erros acima."
    echo ""
    echo "💡 Dicas:"
    echo "   - Use TEST_TYPE=unit para rodar só testes unitários"
    echo "   - Use TEST_TYPE=fast para pular testes lentos"
    echo "   - Veja htmlcov/index.html para coverage detalhado"
    exit $EXIT_CODE
fi
