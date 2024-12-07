from typing import List

from duowen_agent.llm.tokenizer import tokenizer
from duowen_agent.rag.models import Document
from duowen_agent.rag.splitter.comm import split_sentences


class SentenceChunker:
    """
    SentenceChunker splits the sentences in a text based on token limits and sentence boundaries.

    Args:
        chunk_size: Maximum number of tokens per chunk
        chunk_overlap: Number of tokens to overlap between chunks
        min_sentences_per_chunk: Minimum number of sentences per chunk (defaults to 1)

    Raises:
        ValueError: If parameters are invalid
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 128, min_sentences_per_chunk: int = 1):
        """Initialize the SentenceChunker with configuration parameters.

        SentenceChunker splits the sentences in a text based on token limits and sentence boundaries.

        Args:
            chunk_size: Maximum number of tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks
            min_sentences_per_chunk: Minimum number of sentences per chunk (defaults to 1)

        Raises:
            ValueError: If parameters are invalid
        """

        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        if min_sentences_per_chunk < 1:
            raise ValueError("min_sentences_per_chunk must be at least 1")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_sentences_per_chunk = min_sentences_per_chunk

    def _split_sentences(self, text: str) -> List[Document]:
        """Split text into sentences using enhanced regex patterns.

        Handles various cases including:
        - Standard sentence endings across multiple writing systems
        - Quotations and parentheses
        - Common abbreviations
        - Decimal numbers
        - Ellipsis
        - Lists and enumerations
        - Special punctuation
        - Common honorifics and titles

        Args:
            text: Input text to be split into sentences

        Returns:
            List of sentences
        """
        # Define sentence ending punctuation marks from various writing systems

        # Split into sentences and clean up
        sentences = split_sentences(text)

        # Get token counts for sentences
        token_counts = self._get_token_counts(sentences)

        # Create Sentence objects
        result_sentences = []
        current_pos = 0
        for sent, token_count in zip(sentences, token_counts):
            # Find the actual position in original text
            start_idx = text.find(sent, current_pos)
            end_idx = start_idx + len(sent)
            current_pos = end_idx

            result_sentences.append(
                Document(page_content=sent, metadata=dict(start_index=start_idx, end_index=end_idx, token_count=token_count)))

        return result_sentences

    @staticmethod
    def _get_token_counts(sentences: List[str]) -> List[int]:
        """Get token counts for a list of sentences in batch.

        Args:
            sentences: List of sentences

        Returns:
            List of token counts for each sentence
        """
        # Batch encode all sentences at once
        encoded_sentences = tokenizer.emb_encode_batch(sentences)
        return [len(encoded) for encoded in encoded_sentences]

    def _create_chunk(self, sentences: List[Document], start_idx: int, token_count: int) -> Document:
        """Create a chunk from a list of sentences.

        Args:
            sentences: List of sentences to create chunk from
            start_idx: Starting index in original text
            token_count: Total token count for the chunk

        Returns:
            Chunk object
        """
        chunk_text = " ".join([sentence.page_content for sentence in sentences])
        return Document(page_content=chunk_text,
                        metadata=dict(start_index=start_idx, end_index=start_idx + token_count, token_count=token_count,
                                      ))

    def chunk(self, text: str) -> List[Document]:
        """Split text into overlapping chunks based on sentences while respecting token limits.

        Args:
            text: Input text to be chunked

        Returns:
            List of Chunk objects containing the chunked text and metadata
        """
        if not text.strip():
            return []

        sentences = self._split_sentences(text)
        token_counts = [sentence.metadata["token_count"] for sentence in sentences]

        chunks = []
        current_sentences = []
        current_tokens = 0
        last_chunk_end = 0

        for i, (sentence, token_count) in enumerate(zip(sentences, token_counts)):
            # Calculate total tokens if we add this sentence
            test_tokens = (
                    current_tokens + token_count + (1 if current_sentences else 0))  # Add 1 for space between sentences

            can_add_sentence = test_tokens <= self.chunk_size or (
                    len(current_sentences) < self.min_sentences_per_chunk and len(
                current_sentences) + 1 <= self.min_sentences_per_chunk)

            if can_add_sentence:
                # Sentence fits within limits, add it
                current_sentences.append(sentence)
                current_tokens = test_tokens
            else:
                # Sentence would exceed limits, create chunk if we have enough sentences
                if len(current_sentences) >= self.min_sentences_per_chunk:
                    chunk = self._create_chunk(current_sentences, last_chunk_end, current_tokens)
                    chunks.append(chunk)

                    # Calculate overlap for next chunk
                    if self.chunk_overlap > 0:
                        # Keep sentences from the end of current chunk until we hit overlap limit
                        overlap_sentences = []
                        overlap_tokens = 0
                        for sent, tokens in zip(reversed(current_sentences),
                                                reversed(token_counts[i - len(current_sentences): i]), ):
                            test_overlap_tokens = (overlap_tokens + tokens + (1 if overlap_sentences else 0))
                            if test_overlap_tokens <= self.chunk_overlap:
                                overlap_sentences.insert(0, sent)
                                overlap_tokens = test_overlap_tokens
                            else:
                                break

                        current_sentences = overlap_sentences
                        current_tokens = overlap_tokens
                    else:
                        current_sentences = []
                        current_tokens = 0

                    last_chunk_end += current_tokens

                # Add current sentence (either after creating chunk or when forced to meet minimum)
                current_sentences.append(sentence)
                current_tokens = (current_tokens + token_count + (1 if len(current_sentences) > 1 else 0))

        # Handle remaining sentences
        if current_sentences:
            chunk = self._create_chunk(current_sentences, last_chunk_end, current_tokens)
            chunks.append(chunk)

        return chunks

    def __repr__(self) -> str:
        return (f"SentenceChunker(chunk_size={self.chunk_size}, "
                f"chunk_overlap={self.chunk_overlap}, "
                f"min_sentences_per_chunk={self.min_sentences_per_chunk})")
